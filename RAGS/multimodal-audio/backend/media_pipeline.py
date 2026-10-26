"""The media indexing pipeline for one audio or video file.

    Upload → Inspect → Prepare audio → Transcribe → Clean → Chunk
           → Extract frames → Describe frames → Embed → Store

Audio files skip the two frame stages; videos without an audio track skip the
four audio stages. Design rules:

* **Never fail everything for one problem.** If transcription fails, frames can
  still be indexed (and vice versa). The file is then marked `partial`.
* **Never pay twice.** Transcribed audio pieces and frame descriptions are
  cached on disk. A retry only sends the pieces/frames that failed before,
  and re-indexing unchanged media with new chunk settings reuses them.
* **Never leave half a file in ChromaDB.** Records of one collection are
  replaced in one step, and old records are restored if that step fails.
* **Track every stage** in the media registry so the UI can show what
  happened and what can be retried.
"""

from __future__ import annotations

import os
import shutil
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Callable

from backend.audio_processor import AudioPiece, detect_silences, plan_segments, prepare_audio, split_audio
from backend.chunker import get_token_counter
from backend.document_loader import sanitize_filename
from backend.embeddings import EmbeddingService
from backend.frame_analyzer import FrameAnalysis, FrameAnalyzer
from backend.frame_extractor import FrameRecord, detect_scene_changes, extract_frames, plan_frame_timestamps
from backend.media_embeddings import build_frame_chunks, embed_records
from backend.media_registry import (
    STATUS_FAILED,
    STATUS_INDEXED,
    STATUS_PARTIAL,
    STATUS_PROCESSING,
    MediaRegistry,
)
from backend.media_utils import (
    FFmpegTools,
    MediaError,
    MediaInfo,
    StageLog,
    check_media_extension,
    format_time_range,
    media_id_from_hash,
    probe_media,
    save_stream,
    validate_media_info,
)
from backend.media_vector_store import MediaStores
from backend.openai_client import OpenAIServiceError
from backend.transcript_chunker import MEDIA_AUDIO, MEDIA_VIDEO_FRAME, MEDIA_VIDEO_TRANSCRIPT, chunk_transcript
from backend.transcript_cleaner import clean_segments
from backend.transcription_service import TranscriptionService, TranscriptSegment
from backend.document_registry import utc_now
from backend.vector_store import VectorStoreError
from config.settings import ConfigError, validate_chunk_settings

MEDIA_STAGES = [
    ("upload", "Upload", "Save the file and compute its SHA-256 content hash."),
    ("probe", "Inspect", "FFprobe reads duration, streams, codecs and resolution."),
    ("audio", "Prepare audio", "FFmpeg extracts the audio track, converts it and splits it at pauses."),
    ("transcribe", "Transcribe", "OpenAI speech-to-text turns every audio piece into timed text."),
    ("clean", "Clean", "Normalise whitespace without changing meaning, numbers or terms."),
    ("chunk", "Chunk", "Group timed segments into token-limited chunks with overlap."),
    ("frames", "Extract frames", "FFmpeg saves selected keyframes (interval / scene change)."),
    ("vision", "Describe frames", "A vision model describes what is visible on each kept frame."),
    ("embed", "Embed", "The embedding model turns chunks and descriptions into vectors."),
    ("store", "Store", "Records are saved in the persistent ChromaDB media collections."),
]

Progress = Callable[[str, str, float | None], None]  # (stage_key, message, fraction of this stage or None)


@dataclass
class MediaOptions:
    chunk_size: int = 800
    chunk_overlap: int = 120
    frame_interval_seconds: int = 10
    max_frames: int = 500
    analyze_frames: bool = True
    scene_detection: bool = False
    scene_threshold: float = 0.3
    skip_duplicate_frames: bool = True
    image_detail: str = "auto"  # low | auto | high (vision cost vs. ability to read small text)
    reuse_cached_results: bool = True
    replace_previous_versions: bool = True

    def frame_signature(self) -> dict[str, Any]:
        return {
            "frame_interval_seconds": self.frame_interval_seconds,
            "max_frames": self.max_frames,
            "scene_detection": self.scene_detection,
            "scene_threshold": self.scene_threshold,
            "skip_duplicate_frames": self.skip_duplicate_frames,
        }

    def validate(self) -> None:
        validate_chunk_settings(self.chunk_size, self.chunk_overlap)
        if self.frame_interval_seconds < 1:
            raise ConfigError("The frame interval must be at least 1 second.")
        if self.max_frames < 1:
            raise ConfigError("The maximum number of frames must be at least 1.")
        if self.image_detail not in ("low", "auto", "high"):
            raise ConfigError("Image detail must be low, auto or high.")
        if not 0.05 <= self.scene_threshold <= 0.95:
            raise ConfigError("The scene-change threshold must be between 0.05 and 0.95.")


@dataclass
class MediaReport:
    filename: str
    status: str = "pending"  # indexed | partial | duplicate | failed
    document_id: str | None = None
    file_hash: str | None = None
    media_kind: str | None = None
    info: dict[str, Any] = field(default_factory=dict)
    message: str = ""
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    stages: list[StageLog] = field(default_factory=list)
    audio_pieces: int = 0
    segments: int = 0
    transcript_chunks: int = 0
    frames_extracted: int = 0
    frames_described: int = 0
    frames_skipped_duplicate: int = 0
    frames_failed: int = 0
    frame_chunks: int = 0
    embeddings: int = 0
    dimension: int | None = None
    stored_records: int = 0
    seconds: float = 0.0

    def stage(self, key: str) -> StageLog:
        return next(s for s in self.stages if s.key == key)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MediaIndexingPipeline:
    def __init__(
        self,
        registry: MediaRegistry,
        stores: MediaStores,
        tools: FFmpegTools,
        embedder: EmbeddingService | None,
        transcriber: TranscriptionService | None,
        analyzer: FrameAnalyzer | None,
        data_directory: Path,
        *,
        max_upload_bytes: int,
        max_duration_seconds: float,
        audio_chunk_seconds: int = 300,
        timestamp_fallback_seconds: int = 30,
    ):
        self.registry = registry
        self.stores = stores
        self.tools = tools
        self.embedder = embedder
        self.transcriber = transcriber
        self.analyzer = analyzer
        self.data_directory = Path(data_directory)
        self.max_upload_bytes = max_upload_bytes
        self.max_duration_seconds = max_duration_seconds
        self.audio_chunk_seconds = audio_chunk_seconds
        self.timestamp_fallback_seconds = timestamp_fallback_seconds

    # ---------------------------------------------------------------- helpers
    def _abs(self, relative: str) -> Path:
        path = (self.data_directory / relative).resolve()
        if self.data_directory.resolve() not in path.parents:
            raise ValueError("Refusing to read outside the data directory.")
        return path

    def _rel(self, path: Path) -> str:
        return str(Path(path).resolve().relative_to(self.data_directory.resolve()))

    def signature(self, options: MediaOptions) -> dict[str, Any]:
        """Everything that changes the indexed result. Same signature + same hash = duplicate."""
        return {
            "chunk_size": options.chunk_size,
            "chunk_overlap": options.chunk_overlap,
            "analyze_frames": options.analyze_frames,
            **(options.frame_signature() if options.analyze_frames else {}),
            "image_detail": options.image_detail if options.analyze_frames else None,
            "transcription_model": self.transcriber.model if self.transcriber else None,
            "vision_model": self.analyzer.model if (self.analyzer and options.analyze_frames) else None,
            "embedding_model": self.embedder.model if self.embedder else None,
            "audio_chunk_seconds": self.audio_chunk_seconds,
            "timestamp_fallback_seconds": self.timestamp_fallback_seconds,
        }

    # ------------------------------------------------------------------- main
    def process(
        self,
        filename: str,
        source: BinaryIO,
        options: MediaOptions | None = None,
        *,
        force: bool = False,
        progress: Progress | None = None,
    ) -> MediaReport:
        options = options or MediaOptions()
        report = MediaReport(filename=sanitize_filename(filename),
                             stages=[StageLog(key, name) for key, name, _ in MEDIA_STAGES])
        notify = progress or (lambda stage, message, fraction: None)
        started = time.perf_counter()
        timers: dict[str, float] = {}

        def begin(key: str, message: str = "") -> StageLog:
            stage = report.stage(key)
            stage.status = "running"
            timers[key] = time.perf_counter()
            notify(key, message or f"{stage.name}: {report.filename}", None)
            return stage

        def finish(stage: StageLog, status: str, message: str = "", count: int | None = None, **details) -> None:
            stage.status, stage.message, stage.count = status, message, count
            stage.seconds = round(time.perf_counter() - timers.get(stage.key, time.perf_counter()), 3)
            stage.details.update(details)
            if status == "failed":
                report.errors.append(f"{stage.name}: {message}")

        def skip(key: str, message: str) -> None:
            stage = report.stage(key)
            if stage.status == "pending":
                stage.status, stage.message = "skipped", message

        def abort(stage: StageLog, message: str) -> MediaReport:
            finish(stage, "failed", message)
            for s in report.stages:
                if s.status == "pending":
                    s.status, s.message = "skipped", "Not run because an earlier stage failed."
            report.status, report.message = STATUS_FAILED, message
            report.seconds = round(time.perf_counter() - started, 2)
            if report.document_id:
                self._record(report, options, None)
            return report

        # 1. Upload ------------------------------------------------------------
        stage = begin("upload")
        try:
            options.validate()
            extension = check_media_extension(report.filename)
            if self.embedder is None:
                raise ConfigError("OpenAI is not configured (missing OPENAI_API_KEY), so media cannot be indexed.")
            ok, why = self.tools.available()
            if not ok:
                raise MediaError(why)
            uploads = self.registry.uploads_directory
            uploads.mkdir(parents=True, exist_ok=True)
            incoming = uploads / f".incoming-{uuid.uuid4().hex}{extension}"
            file_hash, size = save_stream(source, incoming, self.max_upload_bytes)
        except (MediaError, ConfigError) as exc:
            return abort(stage, str(exc))
        report.file_hash = file_hash
        report.document_id = document_id = media_id_from_hash(file_hash)
        stored_file = f"{document_id}{extension}"
        upload_path = uploads / stored_file
        if upload_path.exists():
            incoming.unlink()  # same hash => the identical file is already stored
        else:
            os.replace(incoming, upload_path)
        finish(stage, "done", f"{size:,} bytes, SHA-256 {file_hash[:12]}…", 1, size_bytes=size, stored_file=stored_file)

        # 2. Probe ---------------------------------------------------------------
        stage = begin("probe")
        existing = self.registry.get(document_id)
        try:
            info = probe_media(upload_path, self.tools)
            report.warnings += validate_media_info(info, extension, self.max_duration_seconds)
        except MediaError as exc:
            if not existing:
                upload_path.unlink(missing_ok=True)
            return abort(stage, str(exc))
        report.media_kind, report.info = info.media_kind, info.to_dict()
        finish(stage, "done", f"{info.media_kind}, {format_time_range(0, info.duration_seconds)}", 1)

        signature = self.signature(options)
        stored_now = self.stores.count_for_document(document_id)
        if (
            existing
            and not force
            and existing.get("status") == STATUS_INDEXED
            and existing.get("signature") == signature
            and sum(stored_now.values()) == existing.get("stored_records")
        ):
            report.status = "duplicate"
            report.message = (
                f"Already indexed as '{existing['filename']}' with the same content and settings "
                f"({existing.get('stored_records', 0)} records). Tick 'Re-index' to process it again."
            )
            report.stored_records = existing.get("stored_records", 0)
            for s in report.stages[2:]:
                s.status, s.message = "skipped", "Duplicate content: already indexed."
            report.seconds = round(time.perf_counter() - started, 2)
            return report

        if not existing or existing.get("status") not in (STATUS_INDEXED, STATUS_PARTIAL):
            # Never mark a still-usable indexed version as "processing".
            self._record(report, options, None, status=STATUS_PROCESSING, stored_file=stored_file)
        transcript_type = MEDIA_AUDIO if info.media_kind == "audio" else MEDIA_VIDEO_TRANSCRIPT

        # 3-6. Audio branch ------------------------------------------------------
        transcript_chunks = []
        if not info.has_audio:
            for key in ("audio", "transcribe", "clean", "chunk"):
                skip(key, "No audio track in this file.")
        elif self.transcriber is None:
            for key in ("audio", "transcribe", "clean", "chunk"):
                skip(key, "Transcription is not configured.")
        else:
            transcript_chunks = self._audio_branch(report, info, upload_path, options, transcript_type, begin, finish, notify)

        # 7-8. Frames branch -----------------------------------------------------
        frame_chunks = []
        if not info.has_video:
            skip("frames", "Audio file: no video stream.")
            skip("vision", "Audio file: no video stream.")
        elif not options.analyze_frames:
            skip("frames", "Frame analysis was turned off for this upload.")
            skip("vision", "Frame analysis was turned off for this upload.")
        elif self.analyzer is None:
            skip("frames", "The vision model is not configured.")
            skip("vision", "The vision model is not configured.")
        else:
            frame_chunks = self._frames_branch(report, info, upload_path, options, begin, finish, notify)

        if not transcript_chunks and not frame_chunks:
            stage = report.stage("embed")
            timers["embed"] = time.perf_counter()
            reason = "; ".join(report.errors) or "no speech and no frame descriptions were produced"
            report.errors.clear()
            return abort(stage, f"Nothing could be indexed: {reason}")

        # 9. Embed -------------------------------------------------------------
        stage = begin("embed")
        embedded: dict[str, Any] = {}
        try:
            self.stores.check_compatible(self.embedder.model)
        except VectorStoreError as exc:
            return abort(stage, str(exc))
        for media_type, records in ((transcript_type, transcript_chunks), (MEDIA_VIDEO_FRAME, frame_chunks)):
            if not records:
                continue
            try:
                embedded[media_type] = embed_records(
                    self.embedder,
                    records,
                    progress=lambda done, total, mt=media_type: notify("embed", f"Embedding {mt}: {done}/{total}", done / total),
                )
            except (OpenAIServiceError, ValueError) as exc:
                report.errors.append(f"Embed ({media_type}): {exc}")
        if not embedded:
            return abort(stage, "; ".join(report.errors[-2:]))
        report.embeddings = sum(len(e.ids) for e in embedded.values())
        report.dimension = next(iter(embedded.values())).dimension
        partial_embed = len(embedded) < sum(1 for r in (transcript_chunks, frame_chunks) if r)
        finish(stage, "partial" if partial_embed else "done",
               f"{report.embeddings} vector(s) × {report.dimension} dims ({self.embedder.model})",
               report.embeddings)

        # 10. Store ------------------------------------------------------------
        stage = begin("store")
        stored = 0
        try:
            for media_type, records in embedded.items():
                stored += self.stores.replace(
                    media_type, document_id, records.ids, records.texts, records.metadatas,
                    records.embeddings, self.embedder.model,
                )
        except (VectorStoreError, ValueError) as exc:
            return abort(stage, f"Storing in ChromaDB failed: {exc}")
        report.stored_records = sum(self.stores.count_for_document(document_id).values())
        finish(stage, "done", f"{stored} record(s) written; {report.stored_records} stored for this file", stored)

        if options.replace_previous_versions:
            for other in self.registry.find_by_filename(report.filename):
                if other["document_id"] != document_id:
                    self.delete_media(other["document_id"])
                    report.warnings.append(
                        f"An older version of '{report.filename}' ({other['document_id']}) was removed from the index."
                    )

        problems = [s for s in report.stages if s.status in ("failed", "partial")]
        report.status = STATUS_PARTIAL if problems else STATUS_INDEXED
        report.seconds = round(time.perf_counter() - started, 2)
        summary = f"{report.transcript_chunks} transcript chunk(s), {report.frame_chunks} frame description(s)"
        report.message = (
            f"Partly indexed ({summary}). Retry to process the failed parts: " + "; ".join(report.errors)
            if problems else f"Indexed {summary} in {report.seconds:.1f}s."
        )
        self._record(report, options, signature, stored_file=stored_file)
        return report

    # --------------------------------------------------------------- branches
    def _audio_branch(self, report, info: MediaInfo, upload_path: Path, options, transcript_type, begin, finish, notify):
        document_id = report.document_id
        transcriber = self.transcriber
        split_seconds = transcriber.split_seconds(self.audio_chunk_seconds, self.timestamp_fallback_seconds)
        trace = self.registry.load_trace(document_id) or {}
        cache_valid = (
            options.reuse_cached_results
            and trace.get("transcription_model") == transcriber.model
            and trace.get("split_seconds") == split_seconds
            and trace.get("language_hint") == (transcriber.language or "")
            and trace.get("prompt") == (transcriber.prompt or "")
            and trace.get("pieces")
        )
        cached: dict[int, list[TranscriptSegment]] = {}
        pieces: list[AudioPiece] = []
        if cache_valid:
            pieces = [AudioPiece(**p) for p in trace["pieces"]]
            for index in trace.get("transcribed_pieces", []):
                cached[index] = [TranscriptSegment.from_dict(s) for s in trace["raw_segments"] if s["piece_index"] == index]

        # 3. Prepare audio (only if some piece still needs transcribing)
        stage = begin("audio")
        audio_dir = self.registry.audio_dir(document_id)
        if pieces and all(p.index in cached for p in pieces):
            finish(stage, "reused", f"All {len(pieces)} piece(s) already transcribed earlier.", len(pieces))
        else:
            try:
                speech = prepare_audio(upload_path, audio_dir / "speech.mp3", self.tools)
                silences = detect_silences(speech, self.tools)
                plan = plan_segments(info.duration_seconds, split_seconds, silences)
                new_pieces = split_audio(speech, plan, audio_dir / "pieces", self.tools)
                for p in new_pieces:
                    p.path = self._rel(Path(p.path))
                if [(p.start_seconds, p.end_seconds) for p in new_pieces] != [(p.start_seconds, p.end_seconds) for p in pieces]:
                    cached = {}  # the split changed, so cached text no longer lines up with the pieces
                pieces = new_pieces
            except MediaError as exc:
                finish(stage, "failed", str(exc))
                for key in ("transcribe", "clean", "chunk"):
                    report.stage(key).status = "skipped"
                return []
            at_silence = sum(p.cut_at_silence for p in pieces[:-1])
            finish(stage, "done",
                   f"{len(pieces)} piece(s) of ≤{split_seconds}s; {at_silence} cut(s) placed in pauses, "
                   f"{len(silences)} pause(s) detected", len(pieces), split_seconds=split_seconds)
            if not transcriber.capabilities.segment_timestamps:
                report.warnings.append(
                    f"'{transcriber.model}' returns text without timestamps, so each transcript segment is timed by "
                    f"the {split_seconds}s audio piece it came from (timing_source = audio_split). Use whisper-1 or "
                    "gpt-4o-transcribe-diarize for segment-level timestamps."
                )
        report.audio_pieces = len(pieces)

        # 4. Transcribe
        stage = begin("transcribe")
        result = transcriber.transcribe_pieces(
            pieces,
            resolve_path=lambda p: self._abs(p.path),
            cached=cached,
            progress=lambda done, total: notify("transcribe", f"Transcribing piece {done}/{total}", done / total),
        )
        transcribed = sorted({p.index for p in pieces} - {f.piece_index for f in result.failures})
        self.registry.save_trace(
            document_id,
            {
                "document_id": document_id,
                "source_file": report.filename,
                "media_type": transcript_type,
                "transcription_model": transcriber.model,
                "response_format": transcriber.capabilities.response_format,
                "timing_source": result.timing_source,
                "language_hint": transcriber.language or "",
                "prompt": transcriber.prompt or "",
                "split_seconds": split_seconds,
                "pieces": [p.to_dict() for p in pieces],
                "transcribed_pieces": transcribed,
                "failures": [asdict(f) for f in result.failures],
                "raw_segments": [s.to_dict() for s in result.segments],
                "clean_segments": [],
                "chunks": [],
                "updated_at": utc_now(),
            },
        )
        reused = len([p for p in pieces if p.index in cached])
        note = f" ({reused} reused from cache)" if reused else ""
        if result.failures and len(result.failures) == len(pieces):
            finish(stage, "failed", result.failures[0].error)
            report.stage("clean").status = report.stage("chunk").status = "skipped"
            return []
        if result.failures:
            finish(stage, "partial",
                   f"{len(pieces) - len(result.failures)}/{len(pieces)} piece(s) transcribed{note}; failed: "
                   + ", ".join(format_time_range(f.start_seconds, f.end_seconds) for f in result.failures),
                   len(result.segments))
            report.errors.append(f"Transcribe: {len(result.failures)} piece(s) failed ({result.failures[0].error})")
        else:
            finish(stage, "reused" if reused == len(pieces) else "done",
                   f"{len(result.segments)} segment(s) from {len(pieces)} piece(s){note}; timing: {result.timing_source}",
                   len(result.segments), model=transcriber.model)
            shutil.rmtree(audio_dir, ignore_errors=True)  # temporary audio is no longer needed
        report.segments = len(result.segments)
        if not result.segments:
            report.stage("clean").status = report.stage("chunk").status = "skipped"
            report.stage("clean").message = "No speech was recognised in the audio."
            report.warnings.append("No speech was recognised in the audio track.")
            return []

        # 5. Clean
        stage = begin("clean")
        cleaned = clean_segments(result.segments)
        finish(stage, "done",
               f"{sum(len(s.text) for s in result.segments):,} → {sum(len(s.text) for s in cleaned):,} characters",
               len(cleaned))

        # 6. Chunk
        stage = begin("chunk")
        chunks = chunk_transcript(
            cleaned,
            document_id=document_id,
            source_file=report.filename,
            file_hash=report.file_hash,
            media_type=transcript_type,
            transcription_model=transcriber.model,
            chunk_size=options.chunk_size,
            chunk_overlap=options.chunk_overlap,
            counter=get_token_counter(),
        )
        report.transcript_chunks = len(chunks)
        finish(stage, "done", f"{len(chunks)} chunk(s) (size {options.chunk_size}, overlap {options.chunk_overlap})",
               len(chunks))

        trace = self.registry.load_trace(document_id) or {}
        trace.update({"clean_segments": [s.to_dict() for s in cleaned], "chunks": [c.to_dict() for c in chunks]})
        self.registry.save_trace(document_id, trace)
        return chunks

    def _frames_branch(self, report, info: MediaInfo, upload_path: Path, options: MediaOptions, begin, finish, notify):
        document_id = report.document_id
        manifest = self.registry.load_frames_manifest(document_id) or {}
        frames: list[FrameRecord] = []
        cached: dict[str, FrameAnalysis] = {}

        # 7. Extract frames
        stage = begin("frames")
        reuse = (
            options.reuse_cached_results
            and manifest.get("options") == options.frame_signature()
            and manifest.get("frames")
            and all(self._abs(f["frame_path"]).exists() for f in manifest["frames"])
        )
        if reuse:
            frames = [FrameRecord.from_dict(f) for f in manifest["frames"]]
            cached = {a["frame_id"]: FrameAnalysis.from_dict(a) for a in manifest.get("analyses", [])}
            finish(stage, "reused", f"{len(frames)} frame(s) from an earlier run.", len(frames))
        else:
            try:
                scene_times = detect_scene_changes(upload_path, self.tools, options.scene_threshold) if options.scene_detection else []
                plan, warnings = plan_frame_timestamps(
                    info.duration_seconds, options.frame_interval_seconds, options.max_frames, scene_times
                )
                report.warnings += warnings
                frames = extract_frames(
                    upload_path,
                    self.registry.frames_dir(document_id),
                    document_id=document_id,
                    source_file=report.filename,
                    plan=plan,
                    tools=self.tools,
                    data_directory=self.data_directory,
                    skip_duplicates=options.skip_duplicate_frames,
                )
            except (MediaError, ValueError) as exc:
                finish(stage, "failed", str(exc))
                report.stage("vision").status = "skipped"
                return []
            dupes = sum(1 for f in frames if f.duplicate_of)
            finish(stage, "done",
                   f"{len(frames)} frame(s), every {options.frame_interval_seconds}s"
                   f"{' + scene changes' if options.scene_detection else ''}; {dupes} near-duplicate(s) will be skipped",
                   len(frames), scene_changes=len(scene_times))
        report.frames_extracted = len(frames)

        # 8. Describe frames
        stage = begin("vision")
        self.analyzer.detail = options.image_detail
        analyses = self.analyzer.analyze_frames(
            frames,
            resolve_path=lambda f: self._abs(f.frame_path),
            cached=cached,
            progress=lambda done, total: notify("vision", f"Describing frame {done}/{total}", done / total),
        )
        self.registry.save_frames_manifest(
            document_id,
            {
                "document_id": document_id,
                "source_file": report.filename,
                "options": options.frame_signature(),
                "vision_model": self.analyzer.model,
                "frames": [f.to_dict() for f in frames],
                "analyses": [a.to_dict() for a in analyses],
                "updated_at": utc_now(),
            },
        )
        done = [a for a in analyses if a.status == "done"]
        failed = [a for a in analyses if a.status == "failed"]
        report.frames_described = len(done)
        report.frames_failed = len(failed)
        report.frames_skipped_duplicate = sum(1 for a in analyses if a.status == "skipped_duplicate")
        reused = sum(1 for a in done if cached.get(a.frame_id) is a)
        message = (
            f"{len(done)} described ({reused} from cache), {report.frames_skipped_duplicate} duplicate(s) skipped, "
            f"{len(failed)} failed — only these {len(frames)} sampled frames were analysed, not every video frame"
        )
        if failed and not done:
            finish(stage, "failed", failed[0].error or message)
            return []
        status = "partial" if failed else ("reused" if done and reused == len(done) else "done")
        finish(stage, status, message, len(done), model=self.analyzer.model)
        if failed:
            report.errors.append(f"Describe frames: {len(failed)} frame(s) failed ({failed[0].error})")
        chunks = build_frame_chunks(frames, analyses, report.file_hash)
        report.frame_chunks = len(chunks)
        return chunks

    # ---------------------------------------------------------------- registry
    def _record(self, report: MediaReport, options: MediaOptions, signature, *, status=None, stored_file=None):
        existing = self.registry.get(report.document_id) or {}
        status = status or report.status
        if status == STATUS_FAILED and existing.get("status") in (STATUS_INDEXED, STATUS_PARTIAL):
            # Keep the previously indexed version usable; only remember the error.
            existing = dict(existing)
            existing.update({"last_error": report.message, "failed_at": utc_now(),
                             "last_stages": [s.to_dict() for s in report.stages]})
            self.registry.upsert(existing)
            return
        trace = self.registry.load_trace(report.document_id) or {}
        record = {
            **existing,
            "document_id": report.document_id,
            "filename": report.filename,
            "file_hash": report.file_hash,
            "media_kind": report.media_kind or existing.get("media_kind"),
            "document_type": report.media_kind or existing.get("media_kind"),
            "stored_file": stored_file or existing.get("stored_file"),
            "info": report.info or existing.get("info", {}),
            "status": status,
            "updated_at": utc_now(),
            "options": asdict(options),
            "stages": [s.to_dict() for s in report.stages],
            "warnings": report.warnings,
            "errors": report.errors,
            "last_error": report.message if status in (STATUS_FAILED, STATUS_PARTIAL) else None,
            "transcription_model": self.transcriber.model if self.transcriber else None,
            "timing_source": trace.get("timing_source"),
            "language": next((s.get("language") for s in trace.get("raw_segments", []) if s.get("language")), None),
            "vision_model": self.analyzer.model if (self.analyzer and options.analyze_frames) else None,
            "embedding_model": self.embedder.model if self.embedder else None,
            "embedding_dimension": report.dimension,
            "audio_pieces": report.audio_pieces,
            "segment_count": report.segments,
            "transcript_chunk_count": report.transcript_chunks,
            "frames_extracted": report.frames_extracted,
            "frames_described": report.frames_described,
            "frames_failed": report.frames_failed,
            "frame_chunk_count": report.frame_chunks,
            "embedding_count": report.embeddings,
            "stored_records": report.stored_records,
            "chunk_count": report.transcript_chunks + report.frame_chunks,
            "processing_seconds": report.seconds,
        }
        if signature is not None:
            record["signature"] = signature
        if status in (STATUS_INDEXED, STATUS_PARTIAL):
            record["indexed_at"] = utc_now()
        self.registry.upsert(record)

    # --------------------------------------------------------------- maintenance
    def delete_media(self, document_id: str) -> int:
        """Remove one media file from every collection, the registry, and disk."""
        removed = self.stores.delete_media(document_id)
        self.registry.remove(document_id)
        return removed

    def reembed_all(self, progress: Progress | None = None) -> list[MediaReport]:
        """After changing the embedding model: empty the media collections and rebuild them.

        Cached transcripts and frame descriptions are reused, so this mostly
        costs embedding calls. A file whose rebuild fails can be retried later
        from the dashboard (its caches are untouched).
        """
        for store in self.stores.stores.values():
            store.reset_collection()
        reports = []
        for record in self.registry.list_documents():
            try:
                reports.append(self.retry(record["document_id"], progress=progress))
            except MediaError as exc:
                reports.append(MediaReport(filename=record["filename"], status=STATUS_FAILED, message=str(exc)))
        return reports

    def retry(self, document_id: str, options: MediaOptions | None = None, progress: Progress | None = None) -> MediaReport:
        """Process a stored upload again; cached transcripts/descriptions are reused."""
        record = self.registry.get(document_id)
        if not record:
            raise MediaError("This media file is not in the registry.")
        path = self.registry.upload_path(record)
        if path is None:
            raise MediaError("The original upload is missing, so it cannot be re-processed. Upload it again.")
        if options is None:
            saved = record.get("options") or {}
            options = MediaOptions(**{k: v for k, v in saved.items() if k in MediaOptions.__dataclass_fields__})
        with open(path, "rb") as handle:
            return self.process(record["filename"], handle, options, force=True, progress=progress)
