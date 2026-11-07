# CKA Study Repo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a CKA study repo (notes, cheat sheet, examples) from the Alta3 "Kubernetes Zero to Hero" video transcript plus missing CKA material from kubernetes.io.

**Architecture:** Markdown notes per CKA domain, shaped like `../terraform_associate`. Video content comes from `source/transcript.txt` split per chapter; gap content comes from kubernetes.io/docs pages fetched and cited. A small Python checker (`scripts/check.py`) is the "test suite": it enforces source tags, link validity, Mermaid fencing and chapter coverage.

**Tech Stack:** Markdown, Mermaid, YAML manifests, Python 3 (stdlib only, run with `.venv/bin/python`), kind for example validation, yt-dlp (already in `.venv`).

**Spec:** `docs/superpowers/specs/2026-11-07-cka-study-repo-design.md`

## Global Constraints

- Video: https://www.youtube.com/watch?v=MTHGoGUFpvE (Alta3 Research, 2h50m). Timestamp link form: `[video MM:SS](https://www.youtube.com/watch?v=MTHGoGUFpvE&t=<seconds>s)`.
- Every `##` topic in a notes file carries at least one source tag: a video timestamp link, or a `https://kubernetes.io/` URL. Both when both apply.
- Domain weights (README order is by weight): Troubleshooting 30, Cluster Architecture/Install/Config 25, Services & Networking 20, Workloads & Scheduling 15, Storage 10. Target Kubernetes v1.37.
- Diagrams are fenced ```` ```mermaid ```` blocks only. No images.
- Code/commands first; no conceptual padding; `Gotchas` heading per note. Paraphrase the video; credit Alta3 Research in README.
- kubernetes.io/docs is a valid source for video-covered topics too, not only gaps: where the transcript is thin or garbled, supplement or correct the section from the matching docs page and tag it with both the timestamp link and the URL. The video's explanation stays the primary framing; docs win on any factual conflict.
- Every command or flag not seen in the transcript must be checked against a fetched kubernetes.io page before it is written. Transcript technical terms are auto-caption output: verify them against docs.
- Pinned chapter table (start seconds): Architecture 102, YAML 1262, Manifests 1492, Making Pods 1735, Namespaces 2040, API Versioning 2338, Resource Monitoring 2503, Requests & Limits 2696, Probes 3061, kubectl exec & cp 3500, ConfigMaps 3934, Volume Mounting 4189, Secrets 4685, Viewing Logs 4876, Labels 5291, Deployments 5761, Storage 6754, Service Basics 7692, Network Policies 8108, Service Port vs TargetPort 8789, ClusterIP 8959, NodePort 9408, LoadBalancer 9555, NodePort Demo 9660, Continued Training 9914.
- Chapter to note-file mapping: Architecture -> 01; YAML, Manifests, Making Pods, Namespaces, API Versioning, Requests & Limits, Probes, kubectl exec & cp, ConfigMaps, Volume Mounting, Secrets, Labels, Deployments -> 02; Service Basics, Network Policies, Port vs TargetPort, ClusterIP, NodePort, LoadBalancer, NodePort Demo -> 03; Storage -> 04; Resource Monitoring, Viewing Logs -> 05; Continued Training -> skipped (promo; listed in video-map as skipped).

## Review Focus

- Transcript mis-hearings (e.g. "cube control", "etc D", "cubelet") leaking into notes: checker rejects a denylist of known mis-hearings.
- A timestamp link whose `t=` lands in the wrong chapter: checker verifies each link falls inside the chapter(s) its note section claims.
- Gap-material commands written from memory (etcd/kubeadm flags especially): each gap section must cite a kubernetes.io URL the checker can see.
- Mermaid block with a syntax error silently rendering as text: checker validates fence balance and a known diagram-type first line.
- Examples that don't apply on a real cluster: each example is validated with `kubectl apply --dry-run=server` on a kind cluster.

---

### Task 1: Scaffold, chapter splitter, checker

**Files:**
- Create: `README.md`, `.gitignore` (extend: add `__pycache__/`, `*.kubeconfig`), `scripts/split_chapters.py`, `scripts/check.py`, `source/chapters/NN-slug.txt` (generated), `notes/video-map.md`
- Test: `scripts/check.py` itself

**Interfaces:**
- Produces: `scripts/check.py` with CLI `python scripts/check.py [--notes notes/] ` exit 0 on pass; functions `check_source_tags(path) -> list[str]`, `check_timestamps(path) -> list[str]`, `check_mermaid(path) -> list[str]`, `check_denylist(path) -> list[str]`, `check_chapter_coverage() -> list[str]` (each returns error strings). `scripts/split_chapters.py` writes one `source/chapters/NN-<slug>.txt` per chapter from `source/transcript.txt` using the pinned chapter table.
- Consumes: `source/transcript.txt` lines of the form `[MM:SS] text`.

- [ ] **Step 1: Write failing checker tests** in `scripts/test_check.py` (stdlib `unittest`): `test_untagged_section_fails` (a `## Pods` section with no link yields an error), `test_tagged_section_passes`, `test_timestamp_outside_declared_chapter_fails`, `test_unbalanced_mermaid_fence_fails`, `test_denylist_flags_"cube control"`.
- [ ] **Step 2: Run** `.venv/bin/python -m unittest scripts/test_check.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3: Implement `scripts/check.py`** with the five functions above. Section declares its chapter via an HTML comment `<!-- chapter: Probes -->`; the checker looks up that chapter's range from the pinned table (copy it into `check.py` as `CHAPTERS: dict[str, tuple[int, int]]`).
- [ ] **Step 4: Run tests again.** Expected: PASS.
- [ ] **Step 5: Implement `scripts/split_chapters.py`**, run it, confirm 25 files exist in `source/chapters/` and the last line of the Architecture chapter file has a timestamp < 21:02.
- [ ] **Step 6: Write `README.md`** (layout table, notes list in weight order, credit to Alta3 Research and the video link, conventions section copied in spirit from `../terraform_associate/README.md`) and `notes/video-map.md` (table: chapter, start link, note file).
- [ ] **Step 7: `git init`, commit** `chore: scaffold CKA study repo with chapter splitter and checker`.

### Task 2: Workloads & Scheduling (`notes/02-workloads-scheduling.md`, `examples/02-workloads/`)

**Files:**
- Create: `notes/02-workloads-scheduling.md`, `examples/02-workloads/*.yaml`, `examples/kind-config.yaml` (1 control-plane + 2 workers)
- Modify: `notes/video-map.md` (confirm rows for the 13 mapped chapters)

**Interfaces:**
- Consumes: `source/chapters/` files for the 13 chapters mapped to 02; `scripts/check.py`.
- Produces: `notes/02-workloads-scheduling.md` with one `##` per video chapter (tagged with `<!-- chapter: ... -->` and timestamp link), plus gap sections each citing kubernetes.io.

- [ ] **Step 1: Read the 13 chapter files**; write one `##` section per chapter: commands and YAML first, Mermaid where it explains a flow (pod lifecycle, rolling update, probe types), `Gotchas` list at the end of the file.
- [ ] **Step 2: Fetch and cite kubernetes.io pages for gap topics**, one `##` each: DaemonSet, StatefulSet, Jobs/CronJobs, rollout/rollback, HPA, ResourceQuota/LimitRange, nodeSelector + affinity, taints/tolerations, static pods, scheduler basics (`nodeName`), Kustomize, Helm basics (check the current CNCF CKA v1.37 curriculum PDF to confirm which of these are in scope; drop out-of-scope ones).
- [ ] **Step 3: Write examples** (`pod-probes.yaml`, `deployment-rolling.yaml`, `configmap-secret-volume.yaml`, `taint-toleration.yaml`, `daemonset.yaml`, `cronjob.yaml`), each linked from the note.
- [ ] **Step 4: Verify.** Run `kind create cluster --config examples/kind-config.yaml`, then `for f in examples/02-workloads/*.yaml; do kubectl apply --dry-run=server -f $f; done`. Expected: every file reports `created (server dry run)`. Then `.venv/bin/python scripts/check.py`. Expected: exit 0.
- [ ] **Step 5: Commit** `docs: add workloads and scheduling notes and examples`.

### Task 3: Services & Networking (`notes/03-services-networking.md`, `examples/03-networking/`)

**Files:**
- Create: `notes/03-services-networking.md`, `examples/03-networking/*.yaml`

**Interfaces:**
- Consumes: chapter files for the 7 chapters mapped to 03; kind cluster from Task 2; `scripts/check.py`.

- [ ] **Step 1: Write video sections** (Service basics, ClusterIP/NodePort/LoadBalancer, port vs targetPort, Network Policies incl. default-deny and allow-from-namespace) with a Mermaid diagram of service type layering and one of packet path via kube-proxy.
- [ ] **Step 2: Gap sections, each citing kubernetes.io**: Ingress + Ingress controllers, Gateway API, CoreDNS and service DNS names, CNI (what it is, where config lives), EndpointSlices, kube-proxy modes.
- [ ] **Step 3: Examples** (`clusterip.yaml`, `nodeport.yaml`, `networkpolicy-default-deny.yaml`, `ingress.yaml`); validate with `--dry-run=server`. Expected: all succeed (Ingress/Gateway CRD-dependent files documented as needing a controller).
- [ ] **Step 4: `check.py` exit 0; commit** `docs: add services and networking notes`.

### Task 4: Storage (`notes/04-storage.md`, `examples/04-storage/`)

**Files:**
- Create: `notes/04-storage.md`, `examples/04-storage/*.yaml`

**Interfaces:**
- Consumes: Storage chapter file (6754-7692s); `scripts/check.py`.

- [ ] **Step 1: Video sections** from the Storage chapter (volumes, PV, PVC binding).
- [ ] **Step 2: Gap sections citing kubernetes.io**: StorageClass and dynamic provisioning, access modes, reclaim policies, volume expansion, `emptyDir`/`hostPath`/projected volumes, volume snapshots (scope-check against curriculum).
- [ ] **Step 3: Examples** (`pv-pvc.yaml`, `storageclass.yaml`, `pod-with-pvc.yaml`); `--dry-run=server`; `check.py` exit 0.
- [ ] **Step 4: Commit** `docs: add storage notes`.

### Task 5: Cluster Architecture, Installation & Configuration (`notes/01-cluster-architecture.md`)

**Files:**
- Create: `notes/01-cluster-architecture.md`

**Interfaces:**
- Consumes: Architecture chapter file (102-1262s); `scripts/check.py`.

- [ ] **Step 1: Video sections** from the Architecture chapter with Mermaid control-plane/worker component diagram and an API request flow sequence diagram.
- [ ] **Step 2: Gap sections, each with exact commands copied from a fetched kubernetes.io page and the URL cited**: kubeadm cluster install, kubeadm upgrade, etcd snapshot save/restore (`etcdctl` flags and cert paths), RBAC (Role, ClusterRole, bindings, `kubectl auth can-i`), kubeconfig and contexts, ServiceAccounts, high-availability topology, CRDs and operators, Helm/Kustomize if not covered in Task 2, container runtime and CNI prerequisites, extension interfaces (CNI/CSI/CRI), certificate management (`kubeadm certs`).
- [ ] **Step 3: Mermaid** upgrade sequence (control plane first, then workers, drain/uncordon) and etcd backup/restore flow.
- [ ] **Step 4: `check.py` exit 0; commit** `docs: add cluster architecture notes`.

### Task 6: Troubleshooting (`notes/05-troubleshooting.md`)

**Files:**
- Create: `notes/05-troubleshooting.md`

**Interfaces:**
- Consumes: Resource Monitoring and Viewing Logs chapter files; `scripts/check.py`.

- [ ] **Step 1: Video sections** (metrics, `kubectl top`, logs including `--previous`, `-f`, multi-container).
- [ ] **Step 2: Gap sections citing kubernetes.io**: `kubectl describe` and events, pod states (`Pending`, `CrashLoopBackOff`, `ImagePullBackOff`) with a Mermaid decision flowchart, node `NotReady` triage, kubelet and container-runtime via `systemctl`/`journalctl`, control-plane component failures (static pod manifests in `/etc/kubernetes/manifests`), service/DNS/network-policy debugging, `kubectl debug`, cluster component logs.
- [ ] **Step 3: `check.py` exit 0; commit** `docs: add troubleshooting notes`.

### Task 7: Exam overview, cheat sheet, final verification

**Files:**
- Create: `notes/00-exam-overview.md`, `cheatsheet.md`
- Modify: `README.md` (finalise notes list), `notes/video-map.md`

**Interfaces:**
- Consumes: all notes from Tasks 2-6.

- [ ] **Step 1: `notes/00-exam-overview.md`**: domain weights table, v1.37, 2h format, allowed docs (kubernetes.io), cite the Linux Foundation CKA page and the CNCF curriculum PDF.
- [ ] **Step 2: `cheatsheet.md`**: imperative kubectl (`run`, `create`, `expose`, `--dry-run=client -o yaml`), `jsonpath`/`custom-columns`, `etcdctl` backup/restore, `kubeadm` upgrade steps, RBAC one-liners, docs-navigation tips; each command traceable to a note section.
- [ ] **Step 3: Full verification.** `.venv/bin/python scripts/check.py` exit 0 and `.venv/bin/python -m unittest scripts/test_check.py` pass; `grep -c "https://www.youtube.com/watch?v=MTHGoGUFpvE&t=" notes/*.md` shows links in 01-05; every one of the 24 non-skipped chapters appears in `video-map.md`.
- [ ] **Step 4: Commit** `docs: add exam overview and cheat sheet`.

---

## Self-review notes

- Spec coverage: domains, source tags, gaps from docs, Mermaid, cheat sheet, examples, git repo, video-map, credit: all mapped to tasks. Non-goals respected (no CKAD-only content; curriculum scope check in Tasks 2/4).
- Builder's call from spec honored: build order Workloads, Services, Storage, Cluster Architecture, Troubleshooting.
- Task 1 order puts `01-cluster-architecture` file in Task 5 by build order; file numbering stays by domain list in the spec.
