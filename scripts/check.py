#!/usr/bin/env python3
"""Checker for the CKA study notes. Exit 0 when every check passes."""
import argparse
import re
import sys
from pathlib import Path

VIDEO_ID = "MTHGoGUFpvE"
VIDEO_END = 10207

_STARTS = [
    ("Architecture", 102), ("YAML", 1262), ("Manifests", 1492),
    ("Making Pods", 1735), ("Namespaces", 2040), ("API Versioning", 2338),
    ("Resource Monitoring", 2503), ("Requests & Limits", 2696),
    ("Probes", 3061), ("kubectl exec & cp", 3500), ("ConfigMaps", 3934),
    ("Volume Mounting", 4189), ("Secrets", 4685), ("Viewing Logs", 4876),
    ("Labels", 5291), ("Deployments", 5761), ("Storage", 6754),
    ("Service Basics", 7692), ("Network Policies", 8108),
    ("Service Port vs TargetPort", 8789), ("ClusterIP", 8959),
    ("NodePort", 9408), ("LoadBalancer", 9555), ("NodePort Demo", 9660),
    ("Continued Training", 9914),
]
CHAPTERS: dict[str, tuple[int, int]] = {
    name: (start, _STARTS[i + 1][1] if i + 1 < len(_STARTS) else VIDEO_END)
    for i, (name, start) in enumerate(_STARTS)
}
SKIPPED_CHAPTERS = {"Continued Training"}

DENYLIST = ["cube control", "cube ctl", "cubelet", "cube adm",
            "cube proxy", "cube DNS"]
# Case-sensitive, word-bounded: plain prose "etc d..." must not match.
DENYLIST_CASE_SENSITIVE = [("etc D", re.compile(r"\betc D(?![A-Za-z])"))]
MERMAID_TYPES = ("graph", "flowchart", "sequenceDiagram", "classDiagram",
                 "stateDiagram", "erDiagram", "gantt", "journey", "pie",
                 "mindmap", "timeline", "gitGraph")

VIDEO_LINK = re.compile(
    r"\[video (\d+):(\d{2})\]\(https://www\.youtube\.com/watch\?v="
    + VIDEO_ID + r"&t=(\d+)s\)")
ANY_YT_T = re.compile(r"youtube\.com/watch\?v=[^\s)]*&t=(\d+)s")
DOCS_URL = re.compile(
    r"https://(?:kubernetes\.io|helm\.sh|training\.linuxfoundation\.org"
    r"|docs\.linuxfoundation\.org|github\.com/cncf/curriculum)/\S+")
CHAPTER_TAG = re.compile(r"<!--\s*chapter:\s*(.+?)\s*-->")


def sections(path):
    """Yield (heading, start_line, body_text) for each '## ' section,
    ignoring headings inside code fences."""
    out, cur, in_fence = [], None, False
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            if cur:
                out.append(cur)
            cur = [line[3:].strip(), n, []]
            continue
        if cur:
            cur[2].append(line)
    if cur:
        out.append(cur)
    return [(h, n, "\n".join(b)) for h, n, b in out]


def check_source_tags(path):
    errs = []
    for head, n, body in sections(path):
        if not (VIDEO_LINK.search(body) or DOCS_URL.search(body)):
            errs.append(f"{path}:{n}: section '{head}' has no video timestamp "
                        "link or kubernetes.io URL")
    return errs


def check_timestamps(path):
    errs = []
    for head, n, body in sections(path):
        tag = CHAPTER_TAG.search(body)
        if not tag:
            continue  # gap section: only needs a URL (check_source_tags)
        name = tag.group(1)
        if name not in CHAPTERS:
            errs.append(f"{path}:{n}: section '{head}' names unknown chapter '{name}'")
            continue
        lo, hi = CHAPTERS[name]
        links = VIDEO_LINK.findall(body)
        if not links:
            errs.append(f"{path}:{n}: section '{head}' is tagged chapter "
                        f"'{name}' but has no video timestamp link")
        for m, s, t in links:
            t = int(t)
            if int(m) * 60 + int(s) != t:
                errs.append(f"{path}:{n}: link text {m}:{s} does not match t={t}s")
            if not lo <= t < hi:
                errs.append(f"{path}:{n}: t={t}s is outside chapter '{name}' "
                            f"[{lo},{hi})")
        for t in ANY_YT_T.findall(body):
            if not any(int(t) == int(x[2]) for x in links):
                errs.append(f"{path}:{n}: malformed video link with t={t}s")
    return errs


def check_mermaid(path):
    errs, opened = [], None
    lines = Path(path).read_text().splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith("```"):
            if opened is None:
                opened = (i + 1, s[3:].strip())
                if opened[1] == "mermaid":
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    first = lines[j].strip() if j < len(lines) else ""
                    if not first.startswith(MERMAID_TYPES):
                        errs.append(f"{path}:{i + 1}: mermaid block does not "
                                    f"start with a known diagram type")
            else:
                opened = None
        i += 1
    if opened:
        errs.append(f"{path}:{opened[0]}: unclosed code fence")
    return errs


def check_denylist(path):
    errs = []
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        low = line.lower()
        for term in DENYLIST:
            if term.lower() in low:
                errs.append(f"{path}:{n}: caption mis-hearing '{term}'")
        for term, rx in DENYLIST_CASE_SENSITIVE:
            if rx.search(line):
                errs.append(f"{path}:{n}: caption mis-hearing '{term}'")
    return errs


def check_chapter_coverage(notes_dir="notes"):
    seen = set()
    for p in Path(notes_dir).glob("*.md"):
        seen.update(CHAPTER_TAG.findall(p.read_text()))
    return [f"chapter '{c}' is not covered by any note section"
            for c in CHAPTERS if c not in seen and c not in SKIPPED_CHAPTERS]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes", default="notes")
    args = ap.parse_args(argv)
    errs = []
    files = sorted(Path(args.notes).glob("*.md"))
    for p in files:
        if p.name == "video-map.md":
            errs += check_denylist(p)
            continue
        for fn in (check_source_tags, check_timestamps, check_mermaid,
                   check_denylist):
            errs += fn(p)
    errs += check_chapter_coverage(args.notes)
    for e in errs:
        print(e)
    print(f"{len(files)} files checked, {len(errs)} problems")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
