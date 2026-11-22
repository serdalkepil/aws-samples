# D2 — Working with AWS Fargate

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M2 S23–S24 (S24 is the hidden demo slide) |
| **Deck status** | Optional. Deck steps: walk through the profile, create a Pod that lands on Fargate, create a Pod that lands on the managed node group. |
| **Time** | 8 minutes |
| **Repo** | `eks-course-demos/d2-fargate/fargate-demo.yaml`, `daemonset-on-fargate.yaml` |
| **Needs** | D0 done (cluster has Fargate profile `fp-demo` for namespace `fargate-demo`) |

## Goal

The **same Pod spec** runs on Fargate or on EC2 depending only on whether it matches a Fargate profile selector. Students see the mutating webhook's work (S22) and the 1:1 Pod-to-node ratio (S25).

## Steps

### 1. Walk through the Fargate profile

```bash
source ~/eks-demo.env
aws eks describe-fargate-profile --cluster-name $CLUSTER --fargate-profile-name fp-demo \
  --query 'fargateProfile.{selectors:selectors,subnets:subnets,podExecutionRole:podExecutionRoleArn,status:status}'
```

**Point out:** the selector (namespace `fargate-demo`, no labels), **private subnets only**, the Pod execution role (lets the Fargate kubelet register and pull images).

Also in the console: EKS → `eks-demo` → **Compute** tab → Fargate profiles.

### 2. Look at the manifest

```bash
cat eks-course-demos/d2-fargate/fargate-demo.yaml
```

**Say:** *"Two identical Pods. The only difference is the namespace."*

### 3. Apply and watch where they land

```bash
kubectl apply -f eks-course-demos/d2-fargate/fargate-demo.yaml
kubectl get pods -A -l app=where-am-i -o wide -w
```

Expected: `on-ec2` Running within seconds on an `ip-192-168-…` node; `on-fargate` Pending for 30–90 seconds, then Running on a node named `fargate-ip-192-168-…`. Press Ctrl-C.

**Say while waiting:** *"Fargate is starting a dedicated microVM for this one Pod. That's the 'improve Pod start time' point on S26: node groups win on start time."*

### 4. Show what the webhook changed

```bash
kubectl get pod on-fargate -n fargate-demo -o yaml | grep -E 'schedulerName|fargate-profile'
#   eks.amazonaws.com/fargate-profile: fp-demo
#   schedulerName: fargate-scheduler

kubectl get pod on-ec2 -o jsonpath='{.spec.schedulerName}{"\n"}'
#   default-scheduler
```

**Say:** *"You didn't write `fargate-scheduler`. The mutating admission webhook added it after checking the profile (S22). That's the same kind of webhook as in the M2 permissions activity."*

### 5. One node per Pod

```bash
kubectl get nodes -L eks.amazonaws.com/compute-type
```

A new node with `compute-type=fargate` appeared just for `on-fargate`.

```bash
kubectl describe node $(kubectl get pod on-fargate -n fargate-demo -o jsonpath='{.spec.nodeName}') | grep -A6 Capacity
```

**Say:** *"Capacity is sized from the Pod's requests (rounded up to a Fargate size). You pay per Pod, not per instance: S25's 'unit of charge'."*

### 6. (Optional, 2 min) What doesn't work on Fargate

```bash
kubectl apply -f eks-course-demos/d2-fargate/daemonset-on-fargate.yaml
kubectl get ds node-agent -n fargate-demo
# DESIRED 0: the DaemonSet targets Fargate nodes only (nodeSelector), and DaemonSets never run on Fargate
```

**Say:** *"No DaemonSets, no privileged Pods, no EBS volumes, no GPUs on Fargate. That's the 'consider node groups to…' list on S26."*

## Bridge to S25–S27

Put S25 on the screen and ask: *"Which of your applications would you put on Fargate?"* (That's the S27 discussion.)

## Cleanup

```bash
kubectl delete -f eks-course-demos/d2-fargate/daemonset-on-fargate.yaml --ignore-not-found
kubectl delete -f eks-course-demos/d2-fargate/fargate-demo.yaml
kubectl get nodes        # the fargate-ip-... node disappears within a minute
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `on-fargate` Pending > 3 min, event mentions profile | Namespace typo, or the profile is still `CREATING` | `aws eks describe-fargate-profile …` status must be `ACTIVE` |
| Fargate Pod stuck `ContainerCreating` | No route to ECR Public from private subnets (NAT missing) | Show the screenshot; move on |
| `on-fargate` landed on EC2 | Applied to the wrong namespace | `kubectl get pod -A -l app=where-am-i` |
