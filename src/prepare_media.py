"""Turns raw videos into light web media for the landing page (media/ folder).

    python3 src/prepare_media.py hero-source RAW [--start S] [--duration 6]
    python3 src/prepare_media.py hero-short  RAW [--start S] [--duration 6]
    python3 src/prepare_media.py short N     RAW [--start S] [--duration 8] [--handle @x] [--caption "..."]  # N = 1, 2 or 3
    python3 src/prepare_media.py thumb N     RAW [--at S]                     # N = 1..6

Then run `python3 src/build.py`: the page uses every file found in media/.
Videos are muted, short loops encoded in H.264 so they autoplay everywhere.
"""

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

MEDIA = Path(__file__).resolve().parent.parent / "media"


def ffmpeg() -> str:
    for candidate in (os.environ.get("FFMPEG"), "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg", shutil.which("ffmpeg")):
        if candidate and Path(candidate).exists():
            return candidate
    raise SystemExit("ffmpeg not found (brew install ffmpeg)")


def cover(w: int, h: int) -> str:
    """Scale and centre-crop to exactly w×h, whatever the source format."""
    return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1"


def encode(raw: Path, out: Path, w: int, h: int, start: float, duration: float) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        ffmpeg(), "-y", "-v", "error", "-ss", str(start), "-t", str(duration), "-i", str(raw),
        "-map", "0:V:0", "-an", "-vf", f"{cover(w, h)},fps=30",
        "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-movflags", "+faststart", str(out),
    ], check=True)
    print(f"✓ {out.relative_to(MEDIA.parent)} ({out.stat().st_size / 1e6:.1f} MB)")


def frame(raw: Path, out: Path, w: int, h: int, at: float) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([ffmpeg(), "-y", "-v", "error", "-ss", str(at), "-i", str(raw),
                    "-frames:v", "1", "-vf", cover(w, h), "-q:v", "4", str(out)], check=True)
    print(f"✓ {out.relative_to(MEDIA.parent)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kind", choices=["hero-source", "hero-short", "short", "thumb"])
    parser.add_argument("args", nargs="+", help="[N] RAW")
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--at", type=float, default=1)
    parser.add_argument("--handle", help="short: creator shown in the app chrome, e.g. @le_corbz")
    parser.add_argument("--caption", help="short: caption shown under the handle")
    a = parser.parse_args()

    if a.kind in ("short", "thumb"):
        if len(a.args) != 2:
            parser.error(f"{a.kind} needs a number and a file, e.g. `{a.kind} 1 clip.mp4`")
        n, raw = int(a.args[0]), Path(a.args[1])
    else:
        n, raw = None, Path(a.args[0])
    if not raw.exists():
        raise SystemExit(f"File not found: {raw}")

    if a.kind == "hero-source":
        encode(raw, MEDIA / "hero-source.mp4", 960, 540, a.start, a.duration or 6)
    elif a.kind == "hero-short":
        encode(raw, MEDIA / "hero-short.mp4", 540, 960, a.start, a.duration or 6)
    elif a.kind == "short":
        encode(raw, MEDIA / f"short-{n}.mp4", 540, 960, a.start, a.duration or 8)
        frame(MEDIA / f"short-{n}.mp4", MEDIA / f"short-{n}.jpg", 540, 960, 0.5)
        if a.handle or a.caption:
            credit = {k: v for k, v in (("handle", a.handle), ("caption", a.caption)) if v}
            (MEDIA / f"short-{n}.json").write_text(json.dumps(credit, ensure_ascii=False), encoding="utf-8")
    else:
        frame(raw, MEDIA / f"thumb-{n}.jpg", 360, 640, a.at)


if __name__ == "__main__":
    main()
