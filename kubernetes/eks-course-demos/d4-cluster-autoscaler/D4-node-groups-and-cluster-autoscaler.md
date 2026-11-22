# D4 — Completing a cluster config: node groups and Cluster Autoscaler

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M3 S15–S16 (S16 is the hidden demo slide). Part B can move to M5 S14–S19. |
| **Deck status** | Optional. Deck steps: create a kubeconfig, an IAM policy for EC2 Auto Scaling, an IAM role for nodes, a managed node group, deploy the Cluster Autoscaler. |
| **Time** | Part A 8 min, Part B 7 min |
| **Repo** | `eks-course-demos/d4-cluster-autoscaler/ca-policy.json`, `inflate.yaml` |
| **Needs** | D0 done. Part B needs Helm. |

## Goal

Part A: the node IAM role and a second managed node group, this time on **Bottlerocket** (the M3 KC1 answer). Part B: Cluster Autoscaler adds a node when Pods are Pending, with IAM through **EKS Pod Identity** instead of the older IRSA steps.

## Part A — kubeconfig, node role, Bottlerocket node group

### A1. kubeconfig

```bash
source ~/eks-demo.env
aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION --alias demo
kubectl get nodes -o wide
```

### A2. The node IAM role eksctl created

```bash
NODE_ROLE=$(aws eks describe-nodegroup --cluster-name $CLUSTER --nodegroup-name mng-default \
  --query 'nodegroup.nodeRole' --output text | awk -F/ '{print $NF}')
aws iam list-attached-role-policies --role-name $NODE_ROLE --query 'AttachedPolicies[].PolicyName'
#   AmazonEKSWorkerNodePolicy, AmazonEC2ContainerRegistryReadOnly (or PullOnly),
#   AmazonEKS_CNI_Policy, AmazonSSMManagedInstanceCore
```

**Say:** *"That's how kubelet registers and how nodes pull from ECR. Remember the M3 bonus KC: Pods on this node can use this role too, unless you block it. Module 9 fixes that with Pod Identity."*

```bash
aws eks list-access-entries --cluster-name $CLUSTER    # the node role has an EC2_LINUX access entry
```

### A3. Add a Bottlerocket managed node group (3–4 min, keep talking)

```bash
eksctl create nodegroup --cluster $CLUSTER --region $AWS_REGION --name mng-bottlerocket \
  --node-type t3.medium --nodes 1 --nodes-min 1 --nodes-max 2 \
  --node-ami-family Bottlerocket --node-private-networking
```

While it runs: EC2 console → Auto Scaling groups → the new `eks-mng-bottlerocket-…` group (S17: "backed by an Auto Scaling group").

```bash
kubectl get nodes -L eks.amazonaws.com/nodegroup -o wide
# OS-IMAGE: Bottlerocket OS ... on the new node
```

**Say:** *"Bottlerocket: open source, built only to run containers, no package manager, updates as whole images. That's KC1 at the end of this module."*

## Part B — Cluster Autoscaler with Pod Identity

### B1. IAM policy for EC2 Auto Scaling

```bash
cat eks-course-demos/d4-cluster-autoscaler/ca-policy.json
POLICY_ARN=$(aws iam create-policy --policy-name EksDemoClusterAutoscaler \
  --policy-document file://eks-course-demos/d4-cluster-autoscaler/ca-policy.json \
  --query Policy.Arn --output text 2>/dev/null || echo arn:aws:iam::$ACCOUNT:policy/EksDemoClusterAutoscaler)
echo $POLICY_ARN
```

**Point out:** the write actions (`SetDesiredCapacity`, `TerminateInstance…`) only work on ASGs tagged `k8s.io/cluster-autoscaler/eks-demo=owned`. Least privilege.

### B2. Give the autoscaler's service account that policy (Pod Identity)

```bash
eksctl create podidentityassociation --cluster $CLUSTER --region $AWS_REGION \
  --namespace kube-system --service-account-name cluster-autoscaler \
  --permission-policy-arns $POLICY_ARN
aws eks list-pod-identity-associations --cluster-name $CLUSTER
```

**Say:** *"No OIDC provider and no trust-policy editing. One association: namespace + service account → role."*

### B3. Install Cluster Autoscaler

```bash
helm repo add autoscaler https://kubernetes.github.io/autoscaler && helm repo update autoscaler
helm upgrade --install cluster-autoscaler autoscaler/cluster-autoscaler -n kube-system \
  --set autoDiscovery.clusterName=$CLUSTER --set awsRegion=$AWS_REGION \
  --set rbac.serviceAccount.name=cluster-autoscaler
CA_DEPLOY=$(kubectl -n kube-system get deploy -o name | grep cluster-autoscaler)
kubectl -n kube-system rollout status $CA_DEPLOY
kubectl -n kube-system logs $CA_DEPLOY | grep -i -m5 'asg\|node group'
```

### B4. Make Pods go Pending and watch a node arrive

```bash
kubectl apply -f eks-course-demos/d4-cluster-autoscaler/inflate.yaml   # starts at 0 replicas
kubectl scale deploy/inflate --replicas=4                             # 1 vCPU each
kubectl get pods -l app=inflate -o wide                               # some Pending
kubectl get nodes -w                                                  # a new node joins in ~1–2 min
```

In another terminal: `kubectl -n kube-system logs -f $CA_DEPLOY | grep -i 'scale-up\|expanding'`.

**Say:** *"Exactly S15 to S16: Pending Pods → CA raises desired capacity on the ASG → new node → Pods scheduled. CA only works inside the min/max of the ASG."*

### B5. Scale in

```bash
kubectl scale deploy/inflate --replicas=0
```

Nodes are removed after about 10 minutes of being unneeded (the M5 scale-in activity). Don't wait in class; check at the next break.

## Cleanup

```bash
kubectl delete -f eks-course-demos/d4-cluster-autoscaler/inflate.yaml
eksctl delete nodegroup --cluster $CLUSTER --region $AWS_REGION --name mng-bottlerocket
# Keep Cluster Autoscaler if you'll run E1 in Module 5; otherwise:
helm uninstall cluster-autoscaler -n kube-system
eksctl delete podidentityassociation --cluster $CLUSTER --region $AWS_REGION \
  --namespace kube-system --service-account-name cluster-autoscaler
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| CA log: `AccessDenied` on autoscaling calls | Association created after the Pod started | `kubectl -n kube-system rollout restart $CA_DEPLOY` |
| CA log: `no node groups found` | ASG not tagged | Check the ASG has `k8s.io/cluster-autoscaler/enabled` and `k8s.io/cluster-autoscaler/eks-demo` tags (D0 config propagates them) |
| No scale-up although Pods Pending | ASG already at max (5) or Pods request more than a t3.medium | Lower replicas/requests |
| Bottlerocket node group fails | Instance type/AMI not offered in that AZ | Try `t3a.medium` or `m5.large` |
