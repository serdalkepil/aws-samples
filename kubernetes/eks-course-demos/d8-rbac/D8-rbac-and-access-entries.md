# D8 — Customizing RBAC roles, then access entries

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M9 S36–S37 (S37 is the hidden demo slide) |
| **Deck status** | Optional. Deck steps: create a Role, create a RoleBinding, bind it to a group, **edit the aws-auth ConfigMap**. This version does the last step with an **access entry** (aws-auth is deprecated) and shows aws-auth only for recognition. |
| **Time** | 10 minutes |
| **Repo** | `eks-course-demos/d8-rbac/dev-rbac.yaml` (+ the IAM JSON used in D0 step 6) |
| **Needs** | D0 done, including the `EksDemoDev` IAM role |

## Goal

RBAC first (Role + RoleBinding to a Kubernetes **group**), tested with impersonation. Then map a real IAM role into that group with an access entry and use it. Finally the no-YAML way: an AWS-managed access policy.

## Steps

### 1. Role and RoleBinding

```bash
source ~/eks-demo.env
cat eks-course-demos/d8-rbac/dev-rbac.yaml
kubectl apply -f eks-course-demos/d8-rbac/dev-rbac.yaml
kubectl -n dev get role,rolebinding
```

**Point out:** the Role lists verbs on `pods` in namespace `dev` only (S24). The RoleBinding's subject is a **Group** named `dev-team` (S25, S28). That's a Kubernetes group name; it doesn't exist in IAM.

### 2. Test RBAC alone with impersonation

```bash
kubectl auth can-i create pods        -n dev     --as jane --as-group dev-team   # yes
kubectl auth can-i create pods        -n default --as jane --as-group dev-team   # no
kubectl auth can-i delete deployments -n dev     --as jane --as-group dev-team   # no
kubectl auth can-i --list -n dev --as jane --as-group dev-team | head
```

**Say:** *"RBAC works. But no real person is in `dev-team` yet. Kubernetes doesn't store users; something has to map an AWS identity to that group."*

### 3. Before: the IAM role can't get in

```bash
aws eks update-kubeconfig --name $CLUSTER --region $AWS_REGION --alias dev-user --user-alias dev-user \
  --role-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev
kubectl config use-context demo          # update-kubeconfig switched to dev-user; stay admin by default
kubectl --context dev-user get pods -n dev
# error: You must be logged in to the server (Unauthorized)
```

Keep `--user-alias dev-user`: without it the command overwrites the user entry the `demo` context uses.

### 4. The old way, for recognition only (S35–S36)

```bash
kubectl -n kube-system get configmap aws-auth -o yaml 2>/dev/null \
  || echo "No aws-auth ConfigMap: this cluster's node groups use access entries"
aws eks describe-cluster --name $CLUSTER --query cluster.accessConfig
# authenticationMode: API_AND_CONFIG_MAP
```

**Say:** *"On older clusters you'd edit that ConfigMap: a YAML typo could lock everyone out, and it's not in CloudTrail. AWS deprecated it. The replacement is an AWS API: access entries."*

### 5. The modern way: an access entry

```bash
aws eks create-access-entry --cluster-name $CLUSTER \
  --principal-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev \
  --kubernetes-groups dev-team
aws eks list-access-entries --cluster-name $CLUSTER
aws eks describe-access-entry --cluster-name $CLUSTER --principal-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev
```

### 6. After: same commands as step 3

```bash
kubectl --context dev-user get pods -n dev                # allowed (empty list)
kubectl --context dev-user run test --image=public.ecr.aws/nginx/nginx:stable -n dev   # allowed
kubectl --context dev-user get pods -n default            # Forbidden
kubectl --context dev-user get nodes                      # Forbidden
kubectl --context dev-user auth whoami                    # the assumed-role ARN and group dev-team
```

**Say:** *"Authentication: IAM (the role). Authorization: RBAC (the group binding). The access entry is the bridge, and it's an API call: CloudTrail, Terraform, CloudFormation."*

### 7. No-YAML alternative: an AWS-managed access policy

```bash
aws eks associate-access-policy --cluster-name $CLUSTER \
  --principal-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev \
  --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy \
  --access-scope type=namespace,namespaces=default
aws eks list-associated-access-policies --cluster-name $CLUSTER --principal-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev
kubectl --context dev-user get pods -n default            # now allowed (view)
kubectl --context dev-user auth can-i delete pods -n default   # no (view only)
```

**Say:** *"Four managed policies cover most needs: ClusterAdmin, Admin, Edit, View, scoped to the cluster or to namespaces. Use groups + RBAC when you need custom rules like our pod-manager Role."*

### 8. Who's cluster admin?

```bash
aws eks list-access-entries --cluster-name $CLUSTER
aws eks list-associated-access-policies --cluster-name $CLUSTER \
  --principal-arn $(aws sts get-caller-identity --query Arn --output text | sed 's#assumed-role/\([^/]*\)/.*#role/\1#; s#:sts:#:iam:#')
```

**Say:** *"The cluster creator got `AmazonEKSClusterAdminPolicy` as a visible access entry. With aws-auth that admin was invisible. That's S40–S42, without `system:masters`."*

## Cleanup

```bash
kubectl config use-context demo
aws eks delete-access-entry --cluster-name $CLUSTER --principal-arn arn:aws:iam::$ACCOUNT:role/EksDemoDev
kubectl delete -f eks-course-demos/d8-rbac/dev-rbac.yaml
kubectl config delete-context dev-user; kubectl config delete-user dev-user
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `Unauthorized` even after step 5 | Your shell can't assume `EksDemoDev` | `aws sts assume-role --role-arn … --role-session-name t` must work (D0 step 6) |
| `Forbidden` on `-n dev` after step 5 | Group name typo between the access entry and the RoleBinding | `aws eks describe-access-entry …` vs `kubectl -n dev get rolebinding -o yaml` |
| Step 8 command errors | Your caller ARN is an IAM user, not a role | Just run `aws eks list-access-entries` and point at the entry |
