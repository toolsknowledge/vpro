"""Speech-to-text with the OpenAI transcription API.

Different models return different amounts of detail, so the app looks up the
capabilities of the configured model and never invents what the model did not
return:

| Model                       | response_format | timestamps          | speakers | language |
|-----------------------------|-----------------|---------------------|----------|----------|
| whisper-1                   | verbose_json    | per segment (model) | no       | yes      |
| gpt-4o-transcribe-diarize   | diarized_json   | per segment (model) | yes      | no       |
| gpt-4o(-mini)-transcribe    | json            | none                | no       | no       |
| gpt-transcribe              | json            | none                | no       | list     |

Fallback for text-only models: the audio is split by FFmpeg into short pieces
(TIMESTAMP_FALLBACK_SECONDS, default 30 s). Each piece's text gets the piece's
start/end time and `timing_source = "audio_split"`. That timing is real (it is
where FFmpeg cut the audio) but only as fine as the piece length, and the UI
says so. Every segment records where its timestamps came from.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from backend.audio_processor import AudioPiece
from backend.openai_client import OpenAIServiceError, call_with_retries

TIMING_MODEL = "model"  # start/end returned by the transcription model
TIMING_AUDIO_SPLIT = "audio_split"  # start/end of the FFmpeg piece the text came from


@dataclass(frozen=True)
class TranscriptionCapabilities:
    response_format: str
    segment_timestamps: bool
    speakers: bool
    language: bool
    extra: tuple[tuple[str, object], ...] = ()
    accepts_prompt: bool = True

    def request_kwargs(self) -> dict:
        kwargs = {"response_format": self.response_format}
        kwargs.update(dict(self.extra))
        return kwargs


def capabilities_for(model: str) -> TranscriptionCapabilities:
    name = (model or "").lower()
    if name.startswith("whisper"):
        return TranscriptionCapabilities(
            "verbose_json", True, False, True, (("timestamp_granularities", ["segment"]),)
        )
    if "diarize" in name:
        # chunking_strategy is required by the API for inputs longer than 30 seconds.
        return TranscriptionCapabilities(
            "diarized_json", True, True, False, (("chunking_strategy", "auto"),), accepts_prompt=False
        )
    # gpt-4o-transcribe, gpt-4o-mini-transcribe, gpt-transcribe and unknown models: plain JSON text.
    return TranscriptionCapabilities("json", False, False, False)


@dataclass
class TranscriptSegment:
    segment_id: str
    piece_index: int
    start_seconds: float
    end_seconds: float
    text: str
    timing_source: str
    speaker: str | None = None
    language: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "TranscriptSegment":
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})


def _get(obj, name, default=None):
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def parse_transcription_response(
    response, piece: AudioPiece, caps: TranscriptionCapabilities, language_hint: str | None = None
) -> list[TranscriptSegment]:
    """Turn one API response for one audio piece into globally-timed segments."""
    if isinstance(response, str):
        text, segments, language = response, None, None
    else:
        text = _get(response, "text", "") or ""
        segments = _get(response, "segments")
        language = _get(response, "language")
        if not language and _get(response, "languages"):
            first = _get(response, "languages")[0]
            language = _get(first, "language") or _get(first, "code") or (first if isinstance(first, str) else None)
    language = language or language_hint or None

    results: list[TranscriptSegment] = []
    if caps.segment_timestamps and segments:
        for i, seg in enumerate(segments):
            seg_text = (_get(seg, "text", "") or "").strip()
            if not seg_text:
                continue
            start = float(_get(seg, "start", 0.0) or 0.0)
            end = float(_get(seg, "end", start) or start)
            # Model timestamps are relative to the piece; add the piece offset. Clamp to the piece.
            g_start = min(piece.end_seconds, piece.start_seconds + max(0.0, start))
            g_end = min(piece.end_seconds, max(g_start, piece.start_seconds + end))
            speaker = _get(seg, "speaker") if caps.speakers else None
            results.append(
                TranscriptSegment(
                    segment_id=f"p{piece.index:04d}s{i:04d}",
                    piece_index=piece.index,
                    start_seconds=round(g_start, 3),
                    end_seconds=round(g_end, 3),
                    text=seg_text,
                    timing_source=TIMING_MODEL,
                    speaker=str(speaker) if speaker else None,
                    language=language,
                )
            )
        return results

    if text.strip():
        results.append(
            TranscriptSegment(
                segment_id=f"p{piece.index:04d}s0000",
                piece_index=piece.index,
                start_seconds=piece.start_seconds,
                end_seconds=piece.end_seconds,
                text=text.strip(),
                timing_source=TIMING_AUDIO_SPLIT,
                language=language,
            )
        )
    return results


@dataclass
class PieceFailure:
    piece_index: int
    start_seconds: float
    end_seconds: float
    error: str


@dataclass
class TranscriptionResult:
    segments: list[TranscriptSegment]
    failures: list[PieceFailure]
    model: str
    capabilities: TranscriptionCapabilities

    @property
    def timing_source(self) -> str:
        sources = {s.timing_source for s in self.segments}
        return sources.pop() if len(sources) == 1 else ("mixed" if sources else "none")


class TranscriptionService:
    def __init__(self, client, model: str, language: str | None = None, max_attempts: int = 3, prompt: str | None = None):
        self.client = client
        self.model = model
        self.language = language or None
        # Optional vocabulary hint ("VPro Skills, RAG, ChromaDB") that helps the model spell domain terms.
        self.prompt = prompt or None
        self.max_attempts = max_attempts
        self.capabilities = capabilities_for(model)

    def split_seconds(self, audio_chunk_seconds: int, fallback_seconds: int) -> int:
        """Piece length to use: short pieces give usable timestamps when the model returns none."""
        return audio_chunk_seconds if self.capabilities.segment_timestamps else fallback_seconds

    def transcribe_piece(self, piece: AudioPiece, path: Path) -> list[TranscriptSegment]:
        kwargs = {"model": self.model, **self.capabilities.request_kwargs()}
        if self.language:
            kwargs["language"] = self.language
        if self.prompt and self.capabilities.accepts_prompt:
            kwargs["prompt"] = self.prompt

        def call():
            with open(path, "rb") as handle:
                return self.client.audio.transcriptions.create(file=handle, **kwargs)

        response = call_with_retries(call, model=self.model, max_attempts=self.max_attempts)
        return parse_transcription_response(response, piece, self.capabilities, self.language)

    def transcribe_pieces(
        self,
        pieces: list[AudioPiece],
        resolve_path: Callable[[AudioPiece], Path],
        progress: Callable[[int, int], None] | None = None,
        cached: dict[int, list[TranscriptSegment]] | None = None,
    ) -> TranscriptionResult:
        """Transcribe every piece. A failed piece is recorded and the rest continue.

        `cached` holds pieces already transcribed in an earlier (partly failed)
        run; those are reused instead of being sent to OpenAI again.
        """
        segments: list[TranscriptSegment] = []
        failures: list[PieceFailure] = []
        for done, piece in enumerate(pieces, start=1):
            if cached and piece.index in cached:
                segments.extend(cached[piece.index])
            else:
                try:
                    segments.extend(self.transcribe_piece(piece, resolve_path(piece)))
                except OpenAIServiceError as exc:
                    failures.append(PieceFailure(piece.index, piece.start_seconds, piece.end_seconds, str(exc)))
                    if not exc.retryable and "rejected the request" not in str(exc):
                        # Wrong key, no credits, unknown model: every other piece would fail the same way.
                        for later in pieces[done:]:
                            failures.append(PieceFailure(later.index, later.start_seconds, later.end_seconds, str(exc)))
                        break
            if progress:
                progress(done, len(pieces))
        segments.sort(key=lambda s: (s.start_seconds, s.segment_id))
        return TranscriptionResult(segments, failures, self.model, self.capabilities)
