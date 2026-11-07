#!/usr/bin/env python3
"""Split source/transcript.txt into source/chapters/NN-<slug>.txt."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check import CHAPTERS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LINE = re.compile(r"^\[(\d+):(\d{2})\]")


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower().replace("&", "and")).strip("-")


def main():
    out = ROOT / "source" / "chapters"
    out.mkdir(parents=True, exist_ok=True)
    buckets = {name: [] for name in CHAPTERS}
    for line in (ROOT / "source" / "transcript.txt").read_text().splitlines():
        m = LINE.match(line)
        if not m:
            continue
        t = int(m.group(1)) * 60 + int(m.group(2))
        for name, (lo, hi) in CHAPTERS.items():
            if lo <= t < hi:
                buckets[name].append(line)
                break
    for i, (name, lines) in enumerate(buckets.items(), 1):
        (out / f"{i:02d}-{slug(name)}.txt").write_text("\n".join(lines) + "\n")
    print(f"wrote {len(buckets)} files to {out}")


if __name__ == "__main__":
    main()
