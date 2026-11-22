# D3 — Deploying a cluster with eksctl

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M3 S12–S13 (S13 is the hidden demo slide) |
| **Deck status** | Optional. Deck steps: install the tools, configure IAM, configure networking, create the cluster. |
| **Time** | 8 minutes. **Don't create a cluster from scratch live**: it takes 15–20 minutes. Show the config and the dry run, then the cluster you made last night (D0). |
| **Repo** | `eks-course-demos/cluster/eks-demo-cluster.yaml`, `eks-prerequisites/install-req-AL2023.sh` |

## Goal

Students see what eksctl does by default (S8) and that a cluster definition is a declarative file that belongs in Git.

## Steps

### 1. Install the tools (show, don't run)

```bash
source ~/eks-demo.env
sed -n '/step 6/,/eksctl installation completed/p' eks-prerequisites/install-req-AL2023.sh
```

**Point out:** the download URL is `github.com/eksctl-io/eksctl` (S9 on the slide still says `weaveworks`), and the checksum check.

### 2. The one-command version (S6) as a dry run

```bash
eksctl create cluster --name preview --region $AWS_REGION --dry-run | less
```

Scroll and point at the defaults eksctl fills in (S8): VPC `192.168.0.0/16` with public + private subnets, a managed node group (`m5.large` by default), IAM roles, **`accessConfig.authenticationMode: API_AND_CONFIG_MAP`**, the Kubernetes version. Quit with `q`.

**Say:** *"Every default is now written down. That's what you'd commit."*

### 3. The file we actually use

```bash
less eks-course-demos/cluster/eks-demo-cluster.yaml
```

Walk it top to bottom, one sentence each:

| Section | Say |
|---|---|
| `metadata` | Name, Region, Kubernetes version (S20: *you* choose minor versions). |
| `accessConfig` | Access entries + aws-auth both on. Module 9 explains why. |
| `iam.withOIDC` | OIDC provider for IRSA; Module 9. |
| `vpc` | Default eksctl VPC, one NAT gateway, API endpoint public + private. |
| `addons` | VPC CNI (with NetworkPolicy), CoreDNS, kube-proxy, Pod Identity agent, EBS CSI, metrics-server: S25 "EKS add-ons". |
| `managedNodeGroups` | 2 × t3.medium on AL2023 in private subnets, tags for Cluster Autoscaler. |
| `fargateProfiles` | Namespace `fargate-demo` → Fargate (D2). |
| `cloudWatch` | Control-plane logs api/audit/authenticator (Module 7). |

### 4. Validate the file

```bash
eksctl create cluster -f eks-course-demos/cluster/eks-demo-cluster.yaml --dry-run | head -30
```

### 5. Show what last night's create produced

```bash
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE \
  --query "StackSummaries[?starts_with(StackName,'eksctl-eks-demo')].StackName"
#   eksctl-eks-demo-cluster
#   eksctl-eks-demo-nodegroup-mng-default
#   (plus addon / fargate stacks)

eksctl get cluster --name $CLUSTER --region $AWS_REGION
eksctl get nodegroup --cluster $CLUSTER --region $AWS_REGION
kubectl get nodes
```

Console tour (60 seconds): **CloudFormation** → the cluster stack's Resources tab (VPC, subnets, roles) → **EKS** → `eks-demo` → Overview (version, platform version, endpoint access) → Compute → Add-ons → **Access** (access entries).

**Say:** *"Two CloudFormation stacks, exactly as S9's output said: one for the control plane, one for the node group. eksctl is a CloudFormation generator with good defaults."*

### 6. Bridge

*"In class: eksctl. At work this is usually Terraform or CDK, often with EKS Blueprints, and reviewed like application code (S17)."*

## Cleanup

Nothing to clean up (the dry run creates nothing).

## If it breaks

| Symptom | Fix |
|---|---|
| Dry run fails on the config file | eksctl version too old for a field or the Kubernetes version. `eksctl version`; upgrade. |
| `--dry-run` asks for credentials | It reads AZs from your account: set the profile/Region. |
| Stacks list is empty | Different Region or account from D0. Check `AWS_REGION` and `aws sts get-caller-identity`. |
