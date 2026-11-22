# E1 — HPA scale-out, then nodes scale out (extra, not in the deck)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M5, after S6 (HPA) or after S18 (Cluster Autoscaler) |
| **Time** | 8 minutes |
| **Repo** | `eks-course-demos/e1-hpa/hpa-demo.yaml` |
| **Needs** | metrics-server (D0). For the node part: Cluster Autoscaler from D4 Part B, still installed. Without it, stop at "Pods Pending" and say *"this is where CA, Karpenter, or Auto Mode takes over"*. |

## Goal

Two control loops chained: the HPA adds Pods when CPU rises; when nodes are full, Pods go Pending and the node autoscaler adds a node.

## Steps

### 1. The app and the HPA

```bash
source ~/eks-demo.env
cat eks-course-demos/e1-hpa/hpa-demo.yaml
kubectl apply -f eks-course-demos/e1-hpa/hpa-demo.yaml
kubectl get hpa php-apache
# TARGETS cpu: 0%/50% (may show <unknown> for ~30 s until metrics arrive)
```

**Point out:** `requests.cpu: 500m` on the container. **Say:** *"The HPA measures utilization against **requests**. No requests, no HPA."* The manifest's HPA is the YAML version of S6's `kubectl autoscale … --cpu-percent=50`.

### 2. Generate load (second terminal)

```bash
kubectl run load --image=public.ecr.aws/docker/library/busybox:stable --restart=Never -- \
  /bin/sh -c "while true; do wget -q -O- http://php-apache >/dev/null; done"
```

### 3. Watch the HPA react (first terminal)

```bash
kubectl get hpa php-apache -w
```

Within 1–2 minutes TARGETS climbs well above 50% and REPLICAS goes 1 → 4 → 8…

**Say:** *"Every 15 seconds: current state vs desired state, act on the difference. The same control loop as Module 1."*

### 4. Pods outgrow the nodes

```bash
kubectl get pods -l app=php-apache -o wide
kubectl top nodes
```

With 2 × t3.medium, some replicas go **Pending** (500m each). If CA is installed:

```bash
kubectl get nodes -w                  # a new node joins after 1–2 minutes
kubectl -n kube-system logs $(kubectl -n kube-system get deploy -o name | grep cluster-autoscaler) | grep -i 'scale-up' | tail -3
```

If the HPA alone doesn't push past node capacity, add pressure with the D4 deployment: `kubectl apply -f eks-course-demos/d4-cluster-autoscaler/inflate.yaml && kubectl scale deploy/inflate --replicas=3`.

### 5. Stop the load and watch scale-in

```bash
kubectl delete pod load
kubectl get hpa php-apache -w
```

Replicas come down after the **5-minute stabilization window** (HPA `behavior` defaults). Nodes come down ~10 minutes after they're empty (the M5 S20–S26 activity, live). Check again at the next break.

## Cleanup

```bash
kubectl delete pod load --ignore-not-found
kubectl delete -f eks-course-demos/e1-hpa/hpa-demo.yaml
kubectl delete -f eks-course-demos/d4-cluster-autoscaler/inflate.yaml --ignore-not-found
```

## If it breaks

| Symptom | Fix |
|---|---|
| TARGETS `<unknown>` for minutes | metrics-server missing: `kubectl top nodes` fails → install it (D0 step 4) |
| Replicas don't rise | Load Pod not running or hitting the wrong Service name: `kubectl logs load` |
| Pending Pods but no new node | No CA installed, or ASG already at max (5) |
