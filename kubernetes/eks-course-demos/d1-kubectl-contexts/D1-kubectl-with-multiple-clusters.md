# D1 — kubectl with more than one cluster

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M1 S33–S34 (hidden demo slide: unhide it) |
| **Deck status** | Optional, "highly recommended if time permits" |
| **Time** | 8 minutes |
| **Repo** | none |
| **Needs** | D0 done. Deck asks for two clusters; this version uses the demo cluster twice (two contexts), which shows the same mechanics for free. A local `kind` cluster works as the second cluster if you have one. |

## Goal

Students see that kubectl doesn't "know" any cluster. It reads a **kubeconfig** file; a **context** = cluster + user + default namespace. Switching context is switching cluster or identity.

## Steps

### 1. Show what kubectl is using right now

```bash
source ~/eks-demo.env
kubectl config get-contexts
kubectl config current-context
kubectl config view --minify
```

**Point at three blocks** in the output: `clusters` (API endpoint + CA), `users` (an `exec` that runs `aws eks get-token`), `contexts` (the pair, plus a namespace).

**Say:** *"kubectl authenticates with your **IAM** identity through `aws eks get-token`. What you're allowed to do is decided inside the cluster by **RBAC**. Keep that split in mind; it comes back on Day 3."*

### 2. Add the cluster under a friendly name

```bash
aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION --alias demo
kubectl config get-contexts           # "demo" is now current
```

### 3. Create a second context with a different default namespace

```bash
kubectl create namespace team-a
kubectl config set-context demo-team-a \
  --cluster "$(kubectl config view --minify -o jsonpath='{.clusters[0].name}')" \
  --user    "$(kubectl config view --minify -o jsonpath='{.users[0].name}')" \
  --namespace team-a
kubectl config get-contexts
```

### 4. Switch and show the difference

```bash
kubectl config use-context demo-team-a
kubectl run hello --image=public.ecr.aws/nginx/nginx:stable
kubectl get pods                      # hello is here (namespace team-a)

kubectl config use-context demo
kubectl get pods                      # empty: default namespace
kubectl get pods -n team-a            # hello again
```

**Ask:** *"Same cluster, same user. What changed?"* (Only the default namespace in the context.)

### 5. Separate kubeconfig files and the `KUBECONFIG` variable

```bash
aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION \
  --kubeconfig ~/.kube/eks-demo.yaml --alias demo-file

KUBECONFIG=~/.kube/eks-demo.yaml kubectl config get-contexts      # only demo-file
export KUBECONFIG=~/.kube/config:~/.kube/eks-demo.yaml
kubectl config get-contexts                                       # merged view: all contexts
unset KUBECONFIG
```

**Say:** *"Teams that manage many clusters keep one file per cluster and merge them with `KUBECONFIG`, or use tools like kubectx. The mechanism is always this."*

### 6. (Optional, 1 min) A context with a different identity

```bash
aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION --alias as-dev --user-alias as-dev \
  --role-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev
kubectl --context as-dev get pods -A
# error: You must be logged in to the server (Unauthorized)   <- expected before D8
kubectl config use-context demo
```

`--user-alias` matters: without it the new user entry overwrites the one `demo` uses, and your admin context starts acting as `EksDemoDev`.

**Say:** *"Authentication worked, IAM gave me a token. But this role has no access entry on the cluster yet. We fix that in Module 9."*

## Cleanup

```bash
kubectl delete namespace team-a
kubectl config delete-context demo-team-a
kubectl config delete-context as-dev 2>/dev/null; kubectl config delete-user as-dev 2>/dev/null
rm -f ~/.kube/eks-demo.yaml
kubectl config use-context demo
```

## If it breaks

| Symptom | Fix |
|---|---|
| `Unauthorized` on the `demo` context | Wrong AWS profile in this shell; `aws sts get-caller-identity` must be the identity that created the cluster. |
| `exec plugin: invalid apiVersion` | Old AWS CLI v1. Use AWS CLI v2. |
| Context names look like ARNs | You skipped `--alias`. Fine; rename with `kubectl config rename-context`. |
