"""Keyframe extraction: save a small, representative set of still images from a video.

A 30-minute video at 30 fps has 54,000 frames. Describing all of them would be
slow and expensive, and almost all would be near-identical. Instead we:

1. Plan timestamps every `interval` seconds (default 10 s). Optionally add
   scene-change moments detected by FFmpeg (`select='gt(scene,0.3)'`).
2. Cap the plan at `max_frames`. If the plan is longer, timestamps are spread
   evenly across the whole video and a warning says the interval was widened.
3. Grab one JPEG per timestamp (FFmpeg fast seek, scaled to max 1280 px wide).
4. Optionally skip near-duplicates: each frame is shrunk to 160×90 grey
   pixels and compared with the previous *kept* frame. If fewer than 0.5 % of
   the pixels changed noticeably, it is the same screen. A static slide filmed
   for two minutes then costs one vision call instead of twelve, while a new
   slide with the same layout but different text is still detected.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

from backend.media_utils import FFmpegTools, MediaError

METHOD_INTERVAL = "interval"
METHOD_SCENE = "scene_change"
_PTS_TIME = re.compile(r"pts_time:\s*([\d.]+)")


@dataclass
class FrameRecord:
    frame_id: str
    document_id: str
    source_file: str
    timestamp_seconds: float
    frame_path: str  # relative to the data directory, never an absolute path
    frame_index: int
    extraction_method: str
    average_hash: str = ""
    duplicate_of: str | None = None  # frame_id of the earlier, near-identical frame

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "FrameRecord":
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})


def plan_frame_timestamps(
    duration: float, interval: float, max_frames: int, extra: list[float] | None = None, min_gap: float = 2.0
) -> tuple[list[tuple[float, str]], list[str]]:
    """Return ([(timestamp, method)], warnings). Pure function."""
    if duration <= 0:
        return [], []
    if interval <= 0:
        raise ValueError("The frame interval must be positive.")
    if max_frames < 1:
        raise ValueError("max_frames must be at least 1.")
    warnings: list[str] = []
    planned = []
    t = 0.0
    while t < duration:
        # The very first frame is often black; sample half a second in.
        planned.append((min(max(t, 0.5), max(duration - 0.05, 0.0)), METHOD_INTERVAL))
        t += interval
    for ts in sorted(extra or []):
        if 0 <= ts < duration and all(abs(ts - p) >= min_gap for p, _ in planned):
            planned.append((ts, METHOD_SCENE))
    planned.sort()

    if len(planned) > max_frames:
        step = duration / max_frames
        warnings.append(
            f"{len(planned)} frames were planned but MAX_FRAMES_PER_VIDEO is {max_frames}; "
            f"sampling one frame every {step:.1f}s instead (scene-change frames dropped)."
        )
        planned = [(min(i * step + step / 2, duration - 0.05), METHOD_INTERVAL) for i in range(max_frames)]
    return [(round(ts, 3), method) for ts, method in planned], warnings


def detect_scene_changes(path: Path, tools: FFmpegTools, threshold: float = 0.3) -> list[float]:
    result = tools.run(
        [
            tools.ffmpeg, "-hide_banner", "-nostdin", "-i", str(path), "-an",
            "-vf", f"select='gt(scene,{threshold})',showinfo", "-f", "null", "-",
        ],
        what="FFmpeg scene detection",
    )
    return parse_scene_times(result.stderr)


def parse_scene_times(stderr: str) -> list[float]:
    return [float(m.group(1)) for line in stderr.splitlines() if "showinfo" in line and (m := _PTS_TIME.search(line))]


def average_hash(image_path: Path, size: int = 8) -> str:
    """64-bit perceptual fingerprint: shrink to 8×8 grey, 1 bit per pixel above the mean."""
    from PIL import Image

    with Image.open(image_path) as img:
        pixels = list(img.convert("L").resize((size, size)).getdata())
    mean = sum(pixels) / len(pixels)
    bits = "".join("1" if p > mean else "0" for p in pixels)
    return f"{int(bits, 2):0{size * size // 4}x}"


def hamming(a: str, b: str) -> int:
    return bin(int(a, 16) ^ int(b, 16)).count("1") if a and b else 64


def changed_fraction(path_a: Path, path_b: Path, size: tuple[int, int] = (160, 90), pixel_threshold: int = 24) -> float:
    """Share of pixels that differ by more than `pixel_threshold` grey levels (0.0 = identical)."""
    from PIL import Image, ImageChops

    with Image.open(path_a) as a, Image.open(path_b) as b:
        diff = ImageChops.difference(a.convert("L").resize(size), b.convert("L").resize(size))
    histogram = diff.histogram()
    return sum(histogram[pixel_threshold + 1:]) / (size[0] * size[1])


def extract_frames(
    video_path: Path,
    out_dir: Path,
    *,
    document_id: str,
    source_file: str,
    plan: list[tuple[float, str]],
    tools: FFmpegTools,
    data_directory: Path,
    skip_duplicates: bool = True,
    duplicate_threshold: float = 0.005,
) -> list[FrameRecord]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("frame_*.jpg"):
        old.unlink()
    records: list[FrameRecord] = []
    last_kept: FrameRecord | None = None
    last_kept_path: Path | None = None
    for index, (ts, method) in enumerate(plan):
        target = out_dir / f"frame_{index:04d}.jpg"
        tools.run(
            [
                tools.ffmpeg, "-hide_banner", "-nostdin", "-y", "-ss", f"{ts:.3f}", "-i", str(video_path),
                "-frames:v", "1", "-an", "-vf", "scale='min(1280,iw)':-2", "-q:v", "3", str(target),
            ],
            timeout=min(tools.timeout, 120),
            what="FFmpeg frame extraction",
        )
        if not target.exists() or target.stat().st_size == 0:
            continue  # seeking past the last decodable frame: skip this timestamp
        fingerprint = average_hash(target)
        record = FrameRecord(
            frame_id=f"{document_id}_f{index:04d}",
            document_id=document_id,
            source_file=source_file,
            timestamp_seconds=ts,
            frame_path=str(target.resolve().relative_to(Path(data_directory).resolve())),
            frame_index=index,
            extraction_method=method,
            average_hash=fingerprint,
        )
        if skip_duplicates and last_kept and changed_fraction(target, last_kept_path) <= duplicate_threshold:
            record.duplicate_of = last_kept.frame_id
        else:
            last_kept, last_kept_path = record, target
        records.append(record)
    if not records:
        raise MediaError("No frames could be extracted from the video stream.")
    return records
