# E2 — NetworkPolicy default deny (extra, not in the deck)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M6 S16–S19 |
| **Time** | 6 minutes |
| **Repo** | `eks-course-demos/e2-network-policy/` (`00-app.yaml`, `10-default-deny.yaml`, `20-allow-client-to-nginx.yaml`) |
| **Needs** | D0 cluster (the VPC CNI add-on has `enableNetworkPolicy: "true"`) |

## Goal

Default allow → default deny (everything breaks, including DNS) → allow exactly client → nginx:80. The S17–S19 three-policy pattern, live, with an "intruder" Pod that stays blocked.

## Steps

### 1. Check enforcement is on

```bash
source ~/eks-demo.env
aws eks describe-addon --cluster-name $CLUSTER --addon-name vpc-cni --query addon.configurationValues
# {"enableNetworkPolicy": "true"}
kubectl get pods -n kube-system -l k8s-app=aws-node -o jsonpath='{.items[0].spec.containers[*].name}{"\n"}'
# aws-node aws-eks-nodeagent   <- the node agent enforces policies with eBPF
```

### 2. Deploy the app: default allow

```bash
kubectl apply -f eks-course-demos/e2-network-policy/00-app.yaml
kubectl -n web wait --for=condition=Ready pod --all --timeout=90s
kubectl -n web exec client   -- wget -qO- -T 3 http://nginx | grep -o '<title>.*</title>'
kubectl -n web exec intruder -- wget -qO- -T 3 http://nginx | grep -o '<title>.*</title>'
# both: <title>Welcome to nginx!</title>
```

**Say:** *"By default every Pod can talk to every Pod, in every namespace (S16)."*

### 3. Default deny (S17)

```bash
cat eks-course-demos/e2-network-policy/10-default-deny.yaml
kubectl apply -f eks-course-demos/e2-network-policy/10-default-deny.yaml
kubectl -n web exec client -- wget -qO- -T 3 http://nginx
# wget: bad address 'nginx'   <- even DNS is blocked now
```

**Say:** *"Egress deny blocks DNS too. That's the first thing that breaks when teams add a deny-all policy in production."*

### 4. Allow exactly what's needed (S18–S19 idea)

```bash
cat eks-course-demos/e2-network-policy/20-allow-client-to-nginx.yaml
kubectl apply -f eks-course-demos/e2-network-policy/20-allow-client-to-nginx.yaml
kubectl -n web exec client   -- wget -qO- -T 3 http://nginx | grep -o '<title>.*</title>'   # works
kubectl -n web exec intruder -- wget -qO- -T 3 http://nginx                                  # bad address / timeout
kubectl -n web get networkpolicy
```

**Point out:** two policies are needed: **egress** from client (to nginx + DNS) and **ingress** to nginx (from client). Selection is by **labels**, not IPs.

### 5. (Optional) Defense in depth

**Say:** *"These stack with security groups (and security groups for Pods, S20). NetworkPolicy filters Pod-to-Pod by labels; security groups filter at the ENI."*

## Cleanup

```bash
kubectl delete namespace web
```

## If it breaks

| Symptom | Fix |
|---|---|
| Step 3 still works (no blocking) | Network policy isn't enabled on the VPC CNI. `aws eks update-addon --cluster-name $CLUSTER --addon-name vpc-cni --configuration-values '{"enableNetworkPolicy":"true"}'`, wait for the aws-node rollout |
| Step 4 client still blocked | DNS rule label mismatch: `kubectl -n kube-system get pods --show-labels | grep coredns` must show `k8s-app=kube-dns` |
