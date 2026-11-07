# CKA Study Repo: Design

Date: 2026-11-07

## Intent

Sharif is preparing for the **CKA** (Certified Kubernetes Administrator, Kubernetes v1.37, 2h exam). He watched "Kubernetes Zero to Hero: The Complete Beginner's Guide (2025 Edition)" (Alta3 Research, instructor Chad, 2h50m, https://www.youtube.com/watch?v=MTHGoGUFpvE), but has no notes or screenshots from it and does not want to rewatch it. The video broke down the confusion he had with CKAD material, so its content must live in the repo. The video is fundamentals only; the CKA goes well beyond it.

Deliverable: a study repo shaped like `../terraform_associate` (code-first notes, cheat sheet, runnable examples), organised by CKA exam domain, combining (a) the video's content and (b) missing CKA material from the official docs.

## Goals

- One notes file per CKA domain, weighted by exam share (Troubleshooting 30, Cluster Architecture/Install/Config 25, Services & Networking 20, Workloads & Scheduling 15, Storage 10).
- Every topic from the video is captured, tagged with a timestamp link, e.g. `[video 41:35](https://www.youtube.com/watch?v=MTHGoGUFpvE&t=2495s)`.
- Every topic added from outside the video is tagged with its kubernetes.io source URL. A reader can always tell video material from added material.
- Gaps are written from kubernetes.io/docs (primarily Tasks and kubeadm sections): kubeadm install and upgrade, etcd backup/restore, RBAC, CNI, node/control-plane troubleshooting, Helm/Kustomize, Gateway/Ingress, etc., per the CNCF curriculum `CKA_Curriculum_v1.37.pdf` (github.com/cncf/curriculum), which is the checklist.
- Diagrams use Mermaid in fenced code blocks.
- `cheatsheet.md`: imperative kubectl, `etcdctl`, `kubeadm`, jsonpath/custom-columns one-liners, docs-navigation tips (kubernetes.io is the only site allowed in the exam).
- `examples/`: manifests that apply to a local kind/minikube cluster, linked from notes.

## Non-goals

- No conceptual padding (what a container is). Quick reference first, per the Terraform repo convention.
- No copying of the video verbatim; paraphrase in own words with own examples. Credit Alta3 Research in the README.
- No CKAD-only material unless it is also in the CKA curriculum.

## Anti-goals

- Unlabelled mixing of video content and added content.
- Stating commands or flags from memory that were not checked against the official docs.
- A repo that only works with a paid cloud account.

## Constraints

- Source of video content: `source/transcript.txt` (auto-captions, `[mm:ss]` lines; may contain mis-transcribed terms, so verify technical terms against docs). Chapters: 25, from K8s Architecture (1:42) through the NodePort demo (ends 165:14) to a closing "Continued Training" chapter (165:14 to 170:07). Chapter start/end seconds come from `yt-dlp --print chapters`.
- Existing: `.venv/` (yt-dlp installed, git-ignored), `source/`.
- Repo conventions copied from `terraform_associate`: README with layout table + credit + conventions; `Gotchas` headings; notes short and scannable.
- Make it a git repo (the Terraform one is). Commit per domain.

## Decisions made with Sharif

- Exam: CKA. Include missing material from official docs. Mermaid for diagrams.
- Organise by exam domain, not video order.

## Builder's calls (my choices, not Sharif's)

- Local cluster tool for examples: **kind** (lightweight, multi-node config; kubeadm-specific topics get docs-sourced commands with a note that kind can't fully reproduce them).
- Build order: Troubleshooting is the largest domain but depends on the others, so write Workloads, Services, Storage (mostly video-backed) first, then Cluster Architecture, then Troubleshooting last. Weight in the README stays by exam share.
- File layout: `notes/00-exam-overview.md`, `01-cluster-architecture.md`, `02-workloads-scheduling.md`, `03-services-networking.md`, `04-storage.md`, `05-troubleshooting.md`, plus `notes/video-map.md` (chapter to note-file index).

## Left to the builder

Exact section breakdown inside each note; which examples earn a manifest; wording.
