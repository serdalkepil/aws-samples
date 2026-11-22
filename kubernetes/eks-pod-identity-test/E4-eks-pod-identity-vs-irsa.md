# E4 — EKS Pod Identity vs IRSA (extra, not in the deck)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M9 S51–S57 (after the IRSA slides) |
| **Time** | 8 minutes |
| **Repo** | `eks-pod-identity-test/pod-identity-demo.md` (full write-up, updated 2026-11-22) and `pod-identity-deployment.yaml` |
| **Needs** | D0 cluster (Pod Identity Agent add-on and OIDC provider both present) |

## Goal

Same outcome two ways: a Pod lists S3 buckets with its **own** IAM role, not the node role. Do it live with Pod Identity; show IRSA as the S54 commands and compare on the whiteboard.

## Steps

### 1. Without anything: the Pod uses the node role

```bash
source ~/eks-demo.env
kubectl run nobody --image=public.ecr.aws/aws-cli/aws-cli:latest --command -- sleep 3600
kubectl wait --for=condition=Ready pod/nobody --timeout=90s
kubectl exec nobody -- aws sts get-caller-identity --query Arn
# ...assumed-role/eksctl-eks-demo-nodegroup-...-NodeInstanceRole-.../i-0abc...
```

**Say:** *"That's the M3 bonus KC: Pods inherit the node role through the instance metadata service. Every Pod on this node gets the same permissions. Not what we want."*

### 2. Create the role (trusts `pods.eks.amazonaws.com`)

```bash
cat eks-pod-identity-test/trust-pod-identity.json
aws iam create-role --role-name pod-identity-s3-example \
  --assume-role-policy-document file://eks-pod-identity-test/trust-pod-identity.json
aws iam attach-role-policy --role-name pod-identity-s3-example \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

**Say:** *"No cluster name, no OIDC URL in this trust policy. The same role works in every cluster in the account."*

### 3. Association + Pod

```bash
aws eks create-pod-identity-association --cluster-name $CLUSTER \
  --namespace default --service-account pod-identity \
  --role-arn arn:aws:iam::$ACCOUNT:role/pod-identity-s3-example
kubectl apply -f eks-pod-identity-test/pod-identity-deployment.yaml
kubectl rollout status deploy/pod-identity
POD=$(kubectl get pod -l app=pod-identity -o jsonpath='{.items[0].metadata.name}')
```

### 4. Test

```bash
kubectl exec $POD -- aws sts get-caller-identity --query Arn
# ...assumed-role/pod-identity-s3-example/eks-eks-demo-pod-identi-...
kubectl exec $POD -- aws s3 ls | head -3
kubectl exec $POD -- env | grep AWS_CONTAINER
kubectl get sa pod-identity -o yaml | grep -c role-arn     # 0: no annotation needed
```

**Say:** *"The Pod Identity webhook injected two variables; the SDK calls the agent on the node, which exchanges the service-account token for credentials. The role session carries tags (cluster, namespace, service account) you can use in IAM conditions."*

### 5. Compare with IRSA (whiteboard, 2 min)

Put S54 on the screen (the `eksctl utils associate-iam-oidc-provider` + `eksctl create iamserviceaccount` commands) and fill the table from the repo write-up:

| | Pod Identity | IRSA |
|---|---|---|
| Per-cluster setup | Agent add-on | OIDC provider |
| Trust policy | `pods.eks.amazonaws.com` (once) | Cluster OIDC issuer (per cluster) |
| Link | EKS API association | SA annotation |
| Session tags | Yes | No |
| Outside EKS | No | Yes |

**Say:** *"AWS recommends Pod Identity on EKS whenever possible. You'll still meet IRSA everywhere: older clusters, many Helm charts, self-managed Kubernetes. Activity question 4 on S65 is IRSA; today its answer E becomes 'a Pod Identity association'."*

## Cleanup

Section 6 of `eks-pod-identity-test/pod-identity-demo.md`, plus:

```bash
kubectl delete pod nobody
```

## If it breaks

| Symptom | Fix |
|---|---|
| Still shows the node role | Association created after the Pod started → `kubectl rollout restart deploy/pod-identity` |
| `AccessDenied` on `s3 ls` | Policy not attached to the role yet (IAM propagation, wait 10 s) |
| No `AWS_CONTAINER_*` variables | Pod Identity Agent add-on missing: `kubectl -n kube-system get ds eks-pod-identity-agent` |
