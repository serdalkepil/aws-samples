# D0 — Demo environment setup (night before Day 1)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **When** | The evening before Day 1. Allow 45 minutes (20 of them waiting for the cluster). |
| **Used by** | Every demo D1–D8 and E1–E5 |
| **Repo** | `~/src/aws-samples/kubernetes/` → `eks-prerequisites/`, `eks-course-demos/cluster/eks-demo-cluster.yaml` |
| **Account** | Your instructor demo account, never a student lab account |
| **Cost** | EKS control plane + 2 × m5.large + 1 NAT gateway while the cluster exists. Delete it after Day 3 (step 9). |

## Step 1 — Workstation

Use your laptop, or an Amazon Linux 2023 EC2 instance if you want a clean demo shell. On AL2023 the repo script installs everything:

```bash
cd ~/src/aws-samples/kubernetes
bash eks-prerequisites/install-req-AL2023.sh       # AWS CLI v2, kubectl, eksctl, Helm, Docker, envsubst
newgrp docker                                     # use docker without sudo in this shell
```

On macOS: `brew install awscli kubectl helm gettext aws/tap/eksctl` plus Docker Desktop.

Check:

```bash
aws --version && kubectl version --client && eksctl version && helm version --short && docker --version
aws sts get-caller-identity                        # the demo account
```

## Step 2 — Session variables (put them in a file you `source` before each demo)

```bash
cat > ~/eks-demo.env <<'EOF'
export CLUSTER=eks-demo
export AWS_REGION=us-east-1
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export REGISTRY=$ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
alias k=kubectl
cd ~/src/aws-samples/kubernetes
EOF
source ~/eks-demo.env
```

## Step 3 — Create the cluster

```bash
eksctl create cluster -f eks-course-demos/cluster/eks-demo-cluster.yaml --dry-run   # validate first; fix anything it rejects
eksctl create cluster -f eks-course-demos/cluster/eks-demo-cluster.yaml             # 15–20 min
```

Expected at the end: `EKS cluster "eks-demo" in "us-east-1" region is ready` and a kubeconfig written.

## Step 4 — Verify the cluster

```bash
kubectl get nodes -o wide -L topology.kubernetes.io/zone
# 2 nodes, Ready, OS-IMAGE Amazon Linux 2023, in two different zones

kubectl get pods -n kube-system
# aws-node, coredns, kube-proxy, ebs-csi-controller/node, eks-pod-identity-agent, metrics-server

aws eks list-addons --cluster-name $CLUSTER
aws eks list-access-entries --cluster-name $CLUSTER
aws eks describe-fargate-profile --cluster-name $CLUSTER --fargate-profile-name fp-demo \
  --query 'fargateProfile.selectors'
kubectl top nodes                                  # metrics-server works
```

If `metrics-server` isn't there (the add-on name was rejected), install it with Helm:

```bash
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server -n kube-system
```

## Step 5 — Pre-build for D5 (ECR) so the live push is fast

```bash
aws ecr create-repository --repository-name nodejs-simple-app \
  --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
cd eks-simple-nodejs-app/simple-nodejs-app
docker build -t nodejs-simple-app:1.0 .            # Apple silicon: add --platform linux/amd64
cd ~/src/aws-samples/kubernetes
```

Don't push yet; the push is the live part of D5.

## Step 6 — IAM role for D8 (access entries)

```bash
envsubst < eks-course-demos/d8-rbac/trust-eksdemodev.json > /tmp/trust.json
envsubst < eks-course-demos/d8-rbac/eksdemodev-policy.json > /tmp/policy.json
aws iam create-role --role-name EksDemoDev --assume-role-policy-document file:///tmp/trust.json
aws iam put-role-policy --role-name EksDemoDev --policy-name describe-eks-demo --policy-document file:///tmp/policy.json
aws sts assume-role --role-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev --role-session-name test --query Credentials.Expiration
```

## Step 7 — Optional pre-installs

- **E3:** CloudWatch Observability add-on (see `E3 - Container Insights and audit logs.md`, step 1). Needs ~10 minutes to show data.
- **E5:** AWS Load Balancer Controller: `bash eks-course-demos/e5-load-balancing/install-lbc.sh` (3 minutes).

## Step 8 — Dry-run every demo once

Run D2, D6, D7, D8 end to end tonight and clean up after each. Take screenshots of the key outputs into a `screenshots/` folder: your fallback if the venue Wi-Fi fails.

## Step 9 — Cleanup after Day 3

```bash
source ~/eks-demo.env
# 1) Load balancers first, WHILE the AWS Load Balancer Controller still runs (it removes them)
kubectl delete -f eks-nginx-traffic-sample/nginx-traffic-sample.yaml --ignore-not-found
kubectl delete -f eks-simple-nginx/nginx-deployment.yaml --ignore-not-found
kubectl get svc -A | grep LoadBalancer; kubectl get ingress -A    # both must be empty
# wait until EC2 → Load Balancers shows no eks-demo NLB/ALB, then:
helm uninstall aws-load-balancer-controller -n kube-system 2>/dev/null
helm uninstall cluster-autoscaler -n kube-system 2>/dev/null
eksctl delete cluster -f eks-course-demos/cluster/eks-demo-cluster.yaml --disable-nodegroup-eviction
aws ecr delete-repository --repository-name nodejs-simple-app --force
aws ecr delete-repository --repository-name eks-nodejs-helm-app --force 2>/dev/null
for p in EksDemoClusterAutoscaler EksDemoAWSLoadBalancerController; do
  aws iam delete-policy --policy-arn arn:aws:iam::$ACCOUNT:policy/$p 2>/dev/null; done
aws iam delete-role-policy --role-name EksDemoDev --policy-name describe-eks-demo
aws iam delete-role --role-name EksDemoDev
# EC2 console: delete any Retained EBS volumes from D7. CloudWatch: delete /aws/eks/eks-demo/cluster.
```
