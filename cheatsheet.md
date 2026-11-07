# CKA Cheat Sheet

Condensed from the notes; every block links to the section it comes from, and that section carries the kubernetes.io citation. Items marked *(not run live)* are destructive procedures that were written from the docs only.

## Shell setup and speed
Source: https://kubernetes.io/docs/reference/kubectl/quick-reference/ ; the exam image already has the `k` alias and completion ([exam overview](notes/00-exam-overview.md#exam-environment-and-allowed-documentation)).

```bash
source <(kubectl completion bash)
alias k=kubectl
complete -o default -F __start_kubectl k
kubectl config get-contexts
kubectl config use-context my-cluster-name
kubectl config set-context --current --namespace=my-namespace   # change default namespace
```

## Imperative kubectl
→ [notes/02-workloads-scheduling.md#kubectl-run-port-forward-exec-and-cp](notes/02-workloads-scheduling.md#kubectl-run-port-forward-exec-and-cp), [#manifest-anatomy](notes/02-workloads-scheduling.md#manifest-anatomy), [#deployments-and-replicasets](notes/02-workloads-scheduling.md#deployments-and-replicasets)

```bash
kubectl run nginx --image=nginx --dry-run=client -o yaml      # generate a Pod manifest
kubectl run demo-pod --image=nginx
kubectl create deployment demo-deploy --image=nginx --replicas=3 --port=80
kubectl scale deployment demo-deploy --replicas=1
kubectl expose deployment demo-deploy --port=80 --target-port=80   # ClusterIP Service
kubectl exec -it demo-pod -- sh
kubectl port-forward pod/demo-pod 2224:80
kubectl cp ./nginx.conf demo-pod:/etc/nginx/nginx.conf
kubectl api-resources            # kinds, short names, apiVersion
kubectl explain deployment.spec.strategy
```

→ [notes/03-services-networking.md#service-basics-a-stable-ip-in-front-of-changing-pods](notes/03-services-networking.md#service-basics-a-stable-ip-in-front-of-changing-pods), [#ingress-and-ingress-controllers](notes/03-services-networking.md#ingress-and-ingress-controllers)

```bash
kubectl create ingress demo --class=nginx --rule="demo.example.com/*=demo-deploy:80"
```

→ [notes/02-workloads-scheduling.md#configmaps](notes/02-workloads-scheduling.md#configmaps), [#secrets](notes/02-workloads-scheduling.md#secrets), [#labels-and-selectors](notes/02-workloads-scheduling.md#labels-and-selectors)

```bash
kubectl create cm app-env --from-literal=LOG_LEVEL=debug --dry-run=client -o yaml
kubectl create configmap dem-heroes --from-file=heroes.txt
kubectl create secret generic app-secret --from-literal=password=s3cret
kubectl get secret db-creds -o jsonpath='{.data.password}' | base64 -d
kubectl label pod demo-pod awesome=sauce          # --overwrite to change; awesome- removes
```

→ [notes/02-workloads-scheduling.md#jobs-and-cronjobs](notes/02-workloads-scheduling.md#jobs-and-cronjobs), [#horizontal-pod-autoscaler](notes/02-workloads-scheduling.md#horizontal-pod-autoscaler), [#resourcequota-and-limitrange](notes/02-workloads-scheduling.md#resourcequota-and-limitrange)

```bash
kubectl create job pi --image=perl:5.34.0 -- perl -Mbignum=bpi -wle 'print bpi(200)'
kubectl create cronjob hello --image=busybox:1.36 --schedule="*/1 * * * *" -- date
kubectl create job manual-run --from=cronjob/hello
kubectl autoscale deployment web --min=2 --max=6 --cpu=50%
kubectl create quota q --hard=requests.cpu=1,limits.cpu=2,pods=10 -n demo --dry-run=client -o yaml
```

Flag references: [kubectl autoscale](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_autoscale/) (`--cpu=80%`), [kubectl create quota](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_quota/) (`--hard=cpu=1,memory=1G,pods=2`), [kubectl create ingress](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_ingress/) (`--class=... --rule="host/path=svc:port"`).

## Rollouts, scheduling
→ [notes/02-workloads-scheduling.md#rollout-rolling-update-and-rollback](notes/02-workloads-scheduling.md#rollout-rolling-update-and-rollback), [#taints-and-tolerations](notes/02-workloads-scheduling.md#taints-and-tolerations), [#nodeselector-node-affinity-and-nodename](notes/02-workloads-scheduling.md#nodeselector-node-affinity-and-nodename)

```bash
kubectl set image deployment/web nginx=nginx:1.27
kubectl rollout status deployment/web
kubectl rollout history deployment/web --revision=2
kubectl rollout undo deployment/web --to-revision=1
kubectl rollout restart deployment/web
kubectl taint nodes cka-study-worker dedicated=batch:NoSchedule     # add; trailing - removes
kubectl label nodes cka-study-worker disktype=ssd
kubectl get pod affinity-demo -o wide
```

## Output formatting (jsonpath, custom-columns, sort)
Source: https://kubernetes.io/docs/reference/kubectl/quick-reference/ , https://kubernetes.io/docs/reference/kubectl/jsonpath/

```bash
kubectl get pods -o=jsonpath='{.items[0].metadata.name}'
kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
kubectl get pods --namespace default --output=custom-columns="NAME:.metadata.name,IMAGE:.spec.containers[*].image"
kubectl get node -o custom-columns='NODE_NAME:.metadata.name,STATUS:.status.conditions[?(@.type=="Ready")].status'
kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'
kubectl get pv --sort-by=.spec.capacity.storage
```

## RBAC one-liners
→ [notes/01-cluster-architecture.md#rbac-roles-clusterroles-bindings](notes/01-cluster-architecture.md#rbac-roles-clusterroles-bindings)

```bash
kubectl create role pod-reader --verb=get --verb=list --verb=watch --resource=pods
kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
kubectl create rolebinding bob-admin-binding --clusterrole=admin --user=bob --namespace=acme
kubectl create rolebinding myapp-view-binding --clusterrole=view --serviceaccount=acme:myapp --namespace=acme
kubectl create clusterrolebinding root-cluster-admin-binding --clusterrole=cluster-admin --user=root
kubectl auth can-i list pods --as=system:serviceaccount:dev:foo -n prod
kubectl auth can-i --list --namespace=foo
```

## kubeconfig
→ [notes/01-cluster-architecture.md#kubeconfig-and-contexts](notes/01-cluster-architecture.md#kubeconfig-and-contexts)

```bash
kubectl config view --minify
kubectl config current-context
kubectl config use-context dev-frontend
```

## etcd backup and restore
→ [notes/01-cluster-architecture.md#etcd-backup-and-restore](notes/01-cluster-architecture.md#etcd-backup-and-restore). Save/status checked live inside the etcd Pod; restore *(not run live)*.

```bash
grep -E -- '--(cert-file|key-file|trusted-ca-file|data-dir|listen-client-urls)' /etc/kubernetes/manifests/etcd.yaml
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=<trusted-ca-file> --cert=<cert-file> --key=<key-file> \
  snapshot save <backup-file-location>
etcdutl --write-out=table snapshot status snapshot.db
etcdutl --data-dir <data-dir-location> snapshot restore snapshot.db     # not run live
# then point /etc/kubernetes/manifests/etcd.yaml hostPath etcd-data at the new dir
```

## kubeadm: create, join, upgrade, certs
→ [notes/01-cluster-architecture.md#create-a-cluster-with-kubeadm](notes/01-cluster-architecture.md#create-a-cluster-with-kubeadm), [#upgrade-a-kubeadm-cluster](notes/01-cluster-architecture.md#upgrade-a-kubeadm-cluster), [#certificate-management-kubeadm-certs](notes/01-cluster-architecture.md#certificate-management-kubeadm-certs). All *(not run live)* except the read-only ones.

```bash
sudo kubeadm init --control-plane-endpoint=<ep> --pod-network-cidr=<cidr>
kubeadm token create --print-join-command
kubeadm certs check-expiration            # read-only
kubeadm certs renew all
```

Upgrade, first control plane node (x = latest patch; the docs say skipping minor versions is unsupported, so go 1.36.x to 1.37.x, or 1.37.x to 1.37.y):

```bash
sudo apt-mark unhold kubeadm && sudo apt-get update && sudo apt-get install -y kubeadm='1.37.x-*' && sudo apt-mark hold kubeadm
sudo kubeadm upgrade plan
sudo kubeadm upgrade apply v1.37.x
kubectl drain <node> --ignore-daemonsets
sudo apt-mark unhold kubelet kubectl && sudo apt-get update && sudo apt-get install -y kubelet='1.37.x-*' kubectl='1.37.x-*' && sudo apt-mark hold kubelet kubectl
sudo systemctl daemon-reload && sudo systemctl restart kubelet
kubectl uncordon <node>
```

Other control plane nodes: `sudo kubeadm upgrade node` instead of `apply`. Workers: upgrade kubeadm, `sudo kubeadm upgrade node`, drain from a control plane node, upgrade kubelet, restart kubelet, uncordon.

## Troubleshooting
→ [notes/05-troubleshooting.md#method-describe-events-logs-then-the-node](notes/05-troubleshooting.md#method-describe-events-logs-then-the-node), [#container-logs-default-container--c---all-containers--f](notes/05-troubleshooting.md#container-logs-default-container--c---all-containers--f), [#more-log-options---previous-selectors---tail---since](notes/05-troubleshooting.md#more-log-options---previous-selectors---tail---since)

```bash
kubectl describe pod <pod>                    # read Events at the bottom
kubectl logs <pod> -c <container> --previous
kubectl logs -l app=web --all-containers --tail=20
kubectl top node
kubectl top pod -A --sort-by=memory
```

→ [notes/05-troubleshooting.md#node-notready-triage](notes/05-troubleshooting.md#node-notready-triage), [#kubelet-and-container-runtime-systemctl-journalctl-crictl](notes/05-troubleshooting.md#kubelet-and-container-runtime-systemctl-journalctl-crictl), [#control-plane-component-failures-static-pods](notes/05-troubleshooting.md#control-plane-component-failures-static-pods)

```bash
kubectl describe node <node>                  # Conditions, Taints, Events
systemctl status kubelet
journalctl -u kubelet --no-pager -n 50
crictl ps -a                                  # works even when the API server is down
crictl logs <container-id>
ls /etc/kubernetes/manifests                  # static pod manifests of the control plane
```

→ [notes/05-troubleshooting.md#services-endpoints-and-dns](notes/05-troubleshooting.md#services-endpoints-and-dns), [#kubectl-debug](notes/05-troubleshooting.md#kubectl-debug)

```bash
kubectl get endpointslices -l kubernetes.io/service-name=web
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
kubectl logs --namespace=kube-system -l k8s-app=kube-dns
kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
kubectl debug myapp -it --copy-to=myapp-debug --container=myapp -- sh
kubectl debug node/mynode -it --image=ubuntu
```

## Storage
→ [notes/04-storage.md#volume-types-emptydir-hostpath-projected](notes/04-storage.md#volume-types-emptydir-hostpath-projected)

```bash
kubectl explain pod.spec.volumes.hostPath.type
kubectl explain pod.spec.volumes.emptyDir
```

PV/PVC/StorageClass manifests: [examples/04-storage/](examples/04-storage/).

## Docs navigation (exam)
- Allowed: kubernetes.io/docs, kubernetes.io/blog, helm.sh/docs, gateway-api.sigs.k8s.io; use the kubernetes.io search box ([exam overview](notes/00-exam-overview.md#exam-environment-and-allowed-documentation)).
- Copy manifests from the docs rather than writing from scratch; `kubectl explain` and `kubectl api-resources` for field names and apiVersion ([notes/02-workloads-scheduling.md#manifest-anatomy](notes/02-workloads-scheduling.md#manifest-anatomy)).
- Ctrl+F in the browser for in-page find; copy/paste in terminal is Ctrl+Shift+C / Ctrl+Shift+V.

## Gotchas
- Static pods (apiserver, etcd, scheduler, controller-manager) cannot be deleted with `kubectl`; move the manifest out of `/etc/kubernetes/manifests/` and back ([notes/01-cluster-architecture.md#certificate-management-kubeadm-certs](notes/01-cluster-architecture.md#certificate-management-kubeadm-certs)).
- `kubectl drain` needs `--ignore-daemonsets`; do not forget `uncordon` ([notes/01-cluster-architecture.md#gotchas](notes/01-cluster-architecture.md#gotchas)).
- Plain `kubectl logs` on a multi-container Pod picks the first container; `kubectl top` needs metrics-server; OOMKilled is exit code 137 in Last State ([notes/05-troubleshooting.md#gotchas](notes/05-troubleshooting.md#gotchas)).
- `roleRef` on a binding cannot be changed; delete and recreate ([notes/01-cluster-architecture.md#rbac-roles-clusterroles-bindings](notes/01-cluster-architecture.md#rbac-roles-clusterroles-bindings)).
- A `mountPath` over an existing directory hides its contents ([notes/02-workloads-scheduling.md#gotchas](notes/02-workloads-scheduling.md#gotchas)).
