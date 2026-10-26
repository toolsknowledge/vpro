"""Create two small demo recordings in sample_files/ for classroom testing.

    python scripts/generate_sample_media.py [--force]

* Python_Lecture.mp4  — six slides (rendered with Pillow) narrated by a
  text-to-speech voice: list comprehensions, embeddings, chunk overlap,
  ChromaDB and RAG evaluation. Use it to test Video RAG (transcript + frames).
* RAG_Evaluation_Session.mp3 — an audio-only "meeting" between two voices
  about evaluating RAG systems. Use it to test Audio RAG.

Speech comes from the macOS `say` command, or `espeak-ng` / `espeak` on
Linux. FFmpeg must be installed. The content is fictional demo material.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "sample_files"
SIZE = (1280, 720)

SLIDES = [
    {
        "title": "Python Lecture: From Lists to RAG",
        "lines": ["VPro Skills EduTech", "Module 4 · Generative AI Engineering"],
        "say": "Welcome to the VPro Skills Python lecture. Today we move from Python list comprehensions "
               "all the way to retrieval augmented generation, and we finish with how to evaluate a RAG system.",
    },
    {
        "title": "List Comprehensions",
        "lines": ["Build a new list in one readable line:"],
        "code": ["squares = [n * n for n in range(10)]", "evens = [n for n in numbers if n % 2 == 0]"],
        "say": "A list comprehension builds a new list in one line. For example, squares equals n times n "
               "for n in range ten. You can add a condition at the end, like keeping only the even numbers. "
               "Use comprehensions when the logic is short; use a normal for loop when it gets complicated.",
    },
    {
        "title": "What Is an Embedding?",
        "lines": ["Text  →  vector of numbers (1536 for text-embedding-3-small)",
                  "Similar meaning  →  vectors close together",
                  "Measured with cosine similarity"],
        "say": "An embedding turns a piece of text into a list of numbers called a vector. The model "
               "text embedding three small produces fifteen hundred and thirty six numbers. Texts with similar "
               "meaning get vectors that point in similar directions, and we measure that with cosine similarity.",
    },
    {
        "title": "Chunk Size and Chunk Overlap",
        "lines": ["Chunk size: about 800 tokens", "Overlap: about 120 tokens",
                  "Overlap keeps sentences that cross a boundary intact"],
        "say": "Before embedding, we split long text into chunks of about eight hundred tokens. Neighbouring "
               "chunks share an overlap of about one hundred and twenty tokens, so a sentence that is cut at a "
               "boundary still appears complete in one of the chunks.",
    },
    {
        "title": "Storing Vectors in ChromaDB",
        "lines": ["PersistentClient keeps data on disk"],
        "code": ["client = chromadb.PersistentClient(path='data/chroma_db')",
                 "collection.upsert(ids=ids, documents=texts, embeddings=vectors)"],
        "say": "ChromaDB is our vector database. A persistent client stores everything on disk, so the index "
               "survives a restart. We upsert the chunk IDs, the chunk text, the metadata and the vectors, and "
               "later we query the collection with the embedding of the question.",
    },
    {
        "title": "Evaluating a RAG System",
        "lines": ["Retrieval: did we fetch the right chunks? (recall at K)",
                  "Faithfulness: is the answer supported by the context?",
                  "Answer relevance: does it answer the question?"],
        "say": "Finally, RAG evaluation. First check retrieval, for example recall at K: did we fetch the right "
               "chunks? Then check faithfulness: is every claim supported by the retrieved context? And check "
               "answer relevance: does the answer actually address the question? Thank you, see you next class.",
    },
]

MEETING = [
    ("A", "Good morning team. Today's session is about RAG evaluation for the student support assistant."),
    ("B", "Thanks. I built a test set of fifty real student questions, each with the document that answers it."),
    ("A", "Great. What was our retrieval recall at five?"),
    ("B", "Recall at five is eighty six percent. Most misses were fee questions where the chunk was split badly."),
    ("A", "So we should try a smaller chunk size, maybe five hundred tokens, and keep the overlap at one hundred."),
    ("B", "Agreed. For faithfulness, the grader found three answers that mentioned a fee not in the context."),
    ("A", "Then we tighten the prompt and require a citation after every sentence. Let's review again next Friday."),
]


def find_tts() -> list[str] | None:
    if shutil.which("say"):
        return ["say"]
    for name in ("espeak-ng", "espeak"):
        if shutil.which(name):
            return [name]
    return None


def speak(tts: list[str], text: str, target: Path, voice: str | None = None) -> None:
    if tts[0] == "say":
        cmd = ["say", "-o", str(target.with_suffix(".aiff"))] + (["-v", voice] if voice else []) + [text]
        subprocess.run(cmd, check=True)
        source = target.with_suffix(".aiff")
    else:
        cmd = tts + (["-v", voice] if voice else []) + ["-w", str(target.with_suffix(".tts.wav")), text]
        subprocess.run(cmd, check=True)
        source = target.with_suffix(".tts.wav")
    ffmpeg(["-i", str(source), "-ac", "1", "-ar", "24000", str(target)])


def ffmpeg(args: list[str]) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-y", *args], check=True)


def duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def font(size: int, mono: bool = False):
    candidates = (
        ["/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
        if mono else
        ["/System/Library/Fonts/Helvetica.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "C:/Windows/Fonts/arial.ttf"]
    )
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_slide(slide: dict, number: int, target: Path) -> None:
    img = Image.new("RGB", SIZE, "#F7F8FC")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, SIZE[0], 120], fill="#4F46E5")
    d.text((60, 32), slide["title"], fill="white", font=font(54))
    y = 175
    for line in slide.get("lines", []):
        d.text((70, y), "• " + line, fill="#1F2937", font=font(36))
        y += 62
    if slide.get("code"):
        y += 20
        d.rounded_rectangle([60, y, SIZE[0] - 60, y + 40 + 52 * len(slide["code"])], 16, fill="#111827")
        for i, line in enumerate(slide["code"]):
            d.text((90, y + 25 + 52 * i), line, fill="#A7F3D0", font=font(30, mono=True))
    d.text((60, SIZE[1] - 50), f"VPro Skills EduTech · slide {number}", fill="#6B7280", font=font(22))
    img.save(target)


def build_lecture(tts, work: Path, target: Path) -> None:
    concat_lines, audio_parts = [], []
    for i, slide in enumerate(SLIDES, start=1):
        wav = work / f"slide{i}.wav"
        speak(tts, slide["say"], wav)
        padded = work / f"slide{i}_pad.wav"
        ffmpeg(["-i", str(wav), "-af", "apad=pad_dur=1.5", str(padded)])  # a pause between slides
        png = work / f"slide{i}.png"
        draw_slide(slide, i, png)
        concat_lines += [f"file '{png.name}'", f"duration {duration(padded):.3f}"]
        audio_parts.append(padded)
    concat_lines.append(f"file 'slide{len(SLIDES)}.png'")  # the concat demuxer needs the last file twice
    (work / "slides.txt").write_text("\n".join(concat_lines) + "\n")
    (work / "audio.txt").write_text("".join(f"file '{p.name}'\n" for p in audio_parts))
    ffmpeg(["-f", "concat", "-safe", "0", "-i", str(work / "audio.txt"), str(work / "narration.wav")])
    ffmpeg([
        "-f", "concat", "-safe", "0", "-i", str(work / "slides.txt"), "-i", str(work / "narration.wav"),
        "-vf", "fps=10,format=yuv420p", "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "96k",
        "-shortest", "-movflags", "+faststart", str(target),
    ])


def build_meeting(tts, work: Path, target: Path) -> None:
    voices = {"A": "Samantha", "B": "Daniel"} if tts[0] == "say" else {"A": "en-us", "B": "en-gb"}
    parts = []
    for i, (speaker, text) in enumerate(MEETING):
        wav = work / f"meet{i}.wav"
        speak(tts, text, wav, voices[speaker])
        padded = work / f"meet{i}_pad.wav"
        ffmpeg(["-i", str(wav), "-af", "apad=pad_dur=0.8", str(padded)])
        parts.append(padded)
    (work / "meeting.txt").write_text("".join(f"file '{p.name}'\n" for p in parts))
    ffmpeg(["-f", "concat", "-safe", "0", "-i", str(work / "meeting.txt"), "-c:a", "libmp3lame", "-b:a", "96k", str(target)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="overwrite existing sample media")
    args = parser.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("FFmpeg is required: see the README section 'Install FFmpeg'.")
        return 1
    tts = find_tts()
    if not tts:
        print("No text-to-speech tool found (macOS `say`, or install espeak-ng on Linux).")
        return 1
    OUT.mkdir(exist_ok=True)
    jobs = [("Python_Lecture.mp4", build_lecture), ("RAG_Evaluation_Session.mp3", build_meeting)]
    for name, build in jobs:
        target = OUT / name
        if target.exists() and not args.force:
            print(f"skip   {name} (exists; use --force to rebuild)")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            build(tts, Path(tmp), target)
        print(f"wrote  {name}  ({duration(target):.0f}s, {target.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
