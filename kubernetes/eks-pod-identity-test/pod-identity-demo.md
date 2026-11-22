# EKS Pod Identity Demo

*Updated 2026-11-22 for the "Running Containers on Amazon EKS" course (Module 9, extra demo E4). Manifest: [`pod-identity-deployment.yaml`](pod-identity-deployment.yaml).*

## Intro

EKS Pod Identity gives Pods their own IAM credentials through the **EKS API**. You don't create an OIDC provider, and the IAM role's trust policy doesn't name a cluster. Instead the role trusts one AWS service principal, `pods.eks.amazonaws.com`, and you link the role to a namespace + service account with a **Pod Identity association**.

Compared with IRSA (IAM roles for service accounts):

| | EKS Pod Identity | IRSA |
|---|---|---|
| Setup per cluster | Pod Identity Agent add-on | IAM OIDC provider |
| Role trust policy | `pods.eks.amazonaws.com`, same for every cluster | The cluster's OIDC issuer, updated for every new cluster |
| Link to the service account | Association in the EKS API | Annotation `eks.amazonaws.com/role-arn` on the service account |
| Session tags (cluster, namespace, SA) | Yes, usable for ABAC | No |
| Works outside EKS | No | Yes (self-managed, ROSA, EKS Anywhere) |

AWS recommends Pod Identity on EKS whenever possible.

### Restrictions

- Use a recent AWS CLI v2 (the Pod Identity commands are newer than old CLI builds).
- Nodes must be Linux on Amazon EC2 (managed, self-managed, or Auto Mode). **Fargate Pods and Windows nodes aren't supported.**
- The AWS SDK in the container must be recent enough to support the container credential provider (all current SDKs and the AWS CLI do).

## 0. Variables

```bash
export CLUSTER=eks-demo
export AWS_REGION=us-east-1
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
```

## 1. Create the IAM role

Trust policy ([`trust-pod-identity.json`](trust-pod-identity.json)). Commands below run from the repo's `kubernetes/` folder.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "pods.eks.amazonaws.com" },
      "Action": ["sts:AssumeRole", "sts:TagSession"]
    }
  ]
}
```

```bash
aws iam create-role --role-name pod-identity-s3-example \
  --assume-role-policy-document file://eks-pod-identity-test/trust-pod-identity.json
aws iam attach-role-policy --role-name pod-identity-s3-example \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

## 2. Install the EKS Pod Identity Agent add-on

Skip this if the cluster already has it (the course demo cluster and EKS Auto Mode do).

```bash
aws eks describe-addon --cluster-name $CLUSTER --addon-name eks-pod-identity-agent 2>/dev/null \
  || aws eks create-addon --cluster-name $CLUSTER --addon-name eks-pod-identity-agent
kubectl get daemonset eks-pod-identity-agent -n kube-system
```

Don't pin `--addon-version`: let EKS choose the default version for your cluster's Kubernetes version.

## 3. Create the Pod Identity association

```bash
aws eks create-pod-identity-association \
  --cluster-name $CLUSTER \
  --namespace default \
  --service-account pod-identity \
  --role-arn arn:aws:iam::$ACCOUNT:role/pod-identity-s3-example

aws eks list-pod-identity-associations --cluster-name $CLUSTER
```

The service account doesn't have to exist yet, and it needs **no annotation**.

## 4. Spin up a test Pod

```bash
kubectl apply -f eks-pod-identity-test/pod-identity-deployment.yaml
kubectl rollout status deploy/pod-identity
```

## 5. Test it

```bash
POD=$(kubectl get pod -l app=pod-identity -o jsonpath='{.items[0].metadata.name}')

# Who am I? Should be the pod-identity-s3-example role, NOT the node role
kubectl exec $POD -- aws sts get-caller-identity

# Uses the role's permissions
kubectl exec $POD -- aws s3 ls

# What the Pod Identity webhook injected
kubectl exec $POD -- env | grep AWS_CONTAINER
#   AWS_CONTAINER_CREDENTIALS_FULL_URI=http://169.254.170.23/v1/credentials
#   AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE=/var/run/secrets/pods.eks.amazonaws.com/serviceaccount/eks-pod-identity-token
```

Optional, to show how it works under the hood (the SDK does exactly this):

```bash
kubectl exec -it $POD -- sh -c \
  'curl -s -H "Authorization: $(cat $AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE)" $AWS_CONTAINER_CREDENTIALS_FULL_URI | head -c 300; echo'
```

The agent on the node (link-local address `169.254.170.23`) exchanges the projected service-account token for temporary credentials. Don't print full credentials on the projector.

## 6. Delete created resources

```bash
kubectl delete -f eks-pod-identity-test/pod-identity-deployment.yaml
ASSOC=$(aws eks list-pod-identity-associations --cluster-name $CLUSTER \
  --namespace default --service-account pod-identity --query 'associations[0].associationId' --output text)
aws eks delete-pod-identity-association --cluster-name $CLUSTER --association-id $ASSOC
aws iam detach-role-policy --role-name pod-identity-s3-example --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam delete-role --role-name pod-identity-s3-example
# Only if you installed the agent just for this demo:
# aws eks delete-addon --cluster-name $CLUSTER --addon-name eks-pod-identity-agent
```
