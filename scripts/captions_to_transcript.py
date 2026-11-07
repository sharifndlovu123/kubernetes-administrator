#!/usr/bin/env python3
"""Convert source/transcript.en-orig.json3 into source/transcript.txt ([MM:SS] text lines).

Usage: python scripts/captions_to_transcript.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def convert(data):
    lines = []
    for ev in data.get("events", []):
        if "segs" not in ev:
            continue
        text = "".join(s.get("utf8", "") for s in ev["segs"]).replace("\n", " ").strip()
        if not text:
            continue
        sec = ev["tStartMs"] / 1000
        lines.append(f"[{int(sec // 60):02d}:{int(sec % 60):02d}] {text}")
    return lines


def main():
    src = ROOT / "source"
    data = json.loads((src / "transcript.en-orig.json3").read_text())
    lines = convert(data)
    (src / "transcript.txt").write_text("\n".join(lines))
    print(f"wrote {len(lines)} lines to {src / 'transcript.txt'}")


if __name__ == "__main__":
    main()
