# Certified Kubernetes Administrator (CKA)

> Code-first study notes, a cheat sheet and runnable examples for the CKA exam (Kubernetes v1.37).

Personal study notes built from the Alta3 Research "Kubernetes Zero to Hero" video, plus gap material from kubernetes.io for CKA topics the video skips.
Commands and manifests first; no conceptual padding.

## Layout

| Path | Purpose |
|------|---------|
| [`cheatsheet.md`](cheatsheet.md) | One-page quick reference: kubectl commands, manifests, gotchas |
| [`notes/`](notes/) | Study notes, one file per CKA domain |
| [`notes/video-map.md`](notes/video-map.md) | Video chapter to note file map, with timestamp links |
| [`examples/`](examples/) | Manifests validated with `kubectl apply --dry-run=server` on a kind cluster |
| [`source/`](source/) | Raw transcript and per-chapter splits (`source/chapters/`) |
| [`scripts/`](scripts/) | `split_chapters.py` and the `check.py` checker |

## Notes by domain (exam weight order)

1. [Troubleshooting](notes/05-troubleshooting.md) (30%)
2. [Cluster architecture, installation and configuration](notes/01-architecture.md) (25%)
3. [Services and networking](notes/03-services-and-networking.md) (20%)
4. [Workloads and scheduling](notes/02-workloads-and-scheduling.md) (15%)
5. [Storage](notes/04-storage.md) (10%)

## Credit

The video-derived notes come from the Alta3 Research course [Kubernetes Zero to Hero](https://www.youtube.com/watch?v=MTHGoGUFpvE) (about 2h50m). Everything is paraphrased in my own words; none of it is a copy of their material. Topics the video does not cover are written from the official docs at [kubernetes.io](https://kubernetes.io/docs/) and cited there.

## Conventions

- Keep each note short and scannable: bullets, tables, code blocks.
- Every `##` section carries a source tag: a video link `[video MM:SS](https://www.youtube.com/watch?v=MTHGoGUFpvE&t=<seconds>s)`, a `https://kubernetes.io/` URL, or both.
- A section drawn from a video chapter has `<!-- chapter: <Chapter Name> -->` and its timestamp must fall inside that chapter. Gap sections have no chapter comment and need only the URL.
- The transcript is auto-captioned; verify technical terms against docs. Docs win on any factual conflict.
- Anything easy to forget goes under a `Gotchas` heading.
- Diagrams are fenced `mermaid` blocks only.
- Run the checker: `.venv/bin/python scripts/check.py` (tests: `.venv/bin/python -m unittest scripts/test_check.py`).
