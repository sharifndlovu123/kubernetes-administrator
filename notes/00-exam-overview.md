# CKA exam overview

Facts about the exam itself. Everything here is from the Linux Foundation pages cited per section; check them again before booking, because the exam changes with each Kubernetes release.

## Format and version
docs: https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/ | https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks

- Online, proctored, performance-based: you solve tasks from a command line against live Kubernetes clusters.
- Duration: 2 hours.
- Kubernetes version: v1.37 (the exam environment tracks the latest minor release, within about 4 to 8 weeks of its release).
- Passing score: 66% or above.
- Proctoring: remote, via streaming audio, video and screen sharing, on PSI's platform with the PSI Secure Browser.
- Results: a score report is emailed within 24 hours of finishing (barring technical difficulties).
- Retake: one retake is included with the purchase (the FAQ says a retake is offered "when eligible" to those who do not pass).
- Validity: 2 years; you have 12 months from purchase to schedule and take the exam.

## Domains and weights
docs: https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/ | https://github.com/cncf/curriculum/blob/main/CKA_Curriculum_v1.37.pdf

| Domain | Weight | Notes in this repo |
|---|---|---|
| Troubleshooting | 30% | [05-troubleshooting.md](05-troubleshooting.md) |
| Cluster Architecture, Installation and Configuration | 25% | [01-cluster-architecture.md](01-cluster-architecture.md) |
| Services and Networking | 20% | [03-services-networking.md](03-services-networking.md) |
| Workloads and Scheduling | 15% | [02-workloads-scheduling.md](02-workloads-scheduling.md) |
| Storage | 10% | [04-storage.md](04-storage.md) |

The CNCF curriculum PDF lists the exact competencies per domain; the notes were scope-checked against it.

## Exam environment and allowed documentation
docs: https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad | https://docs.linuxfoundation.org/tc-docs/certification/certification-resources-allowed

Allowed in the exam's browser (CKA):

- Kubernetes documentation: https://kubernetes.io/docs
- Kubernetes blog: https://kubernetes.io/blog/
- Helm documentation: https://helm.sh/docs
- Gateway API documentation: https://gateway-api.sigs.k8s.io (CKA only)
- Task-specific documentation linked in the exam's Quick Reference box.
- The kubernetes.io search box is allowed; you must not open external search results.

Terminal:

- A Linux terminal; work happens on designated hosts. Connect with `ssh <nodename>`, then `exit` to go back to the base system. Nested ssh is not supported.
- The base system (hostname `base`) does not have the exam tools installed. Do not reboot it: it will not restart your exam environment.
- `sudo -i` gives elevated privileges on any host.
- Preinstalled: `kubectl` (with the `k` alias and Bash autocompletion), `yq`, `curl`, `wget`, `man`.
- Copy/paste in the terminal: Ctrl+Shift+C / Ctrl+Shift+V (or right-click menu).
- Use Ctrl+Alt+W instead of Ctrl+W (which would close the Chrome tab). The Insert key is prohibited; in vim press `i` for insert mode and Esc to leave it.

Not fetched / left out: how many terminals or browser tabs are allowed (the tips page does not say), and exact task counts (not published on the pages above).

## How to use this repo

docs: https://kubernetes.io/docs/ | video: [video 01:42](https://www.youtube.com/watch?v=MTHGoGUFpvE&t=102s)

- Study in weight order: the README lists the notes that way. Troubleshooting and cluster administration are 55% of the exam together.
- Each note is code-first with a `Gotchas` section at the end. Every `##` section is tagged with a video timestamp link, a kubernetes.io URL, or both.
- Video timestamps: the Alta3 Research video covers workloads, services and storage, and only parts of cluster architecture and troubleshooting. [video-map.md](video-map.md) maps every chapter to a note with a timestamp link; the rest (kubeadm, etcd, RBAC, scheduling, CoreDNS and more) is gap material from kubernetes.io, marked `<!-- gap -->`.
- kind: manifests and read-only commands were checked live on a local kind cluster (`examples/kind-config.yaml`). Destructive procedures (`kubeadm init/join/upgrade/reset`, etcd restore, certificate renewal) were not run live and are marked "not run live".
- [../cheatsheet.md](../cheatsheet.md) condenses the commands, each linked back to the note section it comes from.
- Examples in [../examples/](../examples/) are validated with `kubectl apply --dry-run=server`.
