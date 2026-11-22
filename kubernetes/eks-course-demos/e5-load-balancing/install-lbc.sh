#!/usr/bin/env bash
# Install the AWS Load Balancer Controller on the demo cluster with EKS Pod Identity (extra demo E5).
# Not needed on EKS Auto Mode clusters (load balancing is built in).
# Usage: CLUSTER=eks-demo AWS_REGION=us-east-1 ./install-lbc.sh
set -euo pipefail
CLUSTER=${CLUSTER:-eks-demo}
AWS_REGION=${AWS_REGION:-us-east-1}
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
VPC_ID=$(aws eks describe-cluster --name "$CLUSTER" --region "$AWS_REGION" --query cluster.resourcesVpcConfig.vpcId --output text)

helm repo add eks https://aws.github.io/eks-charts >/dev/null 2>&1 || true
helm repo update eks >/dev/null

# IAM policy published with the controller. Use the policy from the same release as the chart's appVersion.
LBC_VERSION=${LBC_VERSION:-$(helm show chart eks/aws-load-balancer-controller | awk '/^appVersion:/{print $2}')}
echo "AWS Load Balancer Controller $LBC_VERSION"
curl -fsSL -o /tmp/lbc-iam-policy.json \
  "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/${LBC_VERSION}/docs/install/iam_policy.json"

POLICY_ARN=arn:aws:iam::$ACCOUNT:policy/EksDemoAWSLoadBalancerController
aws iam get-policy --policy-arn "$POLICY_ARN" >/dev/null 2>&1 \
  || aws iam create-policy --policy-name EksDemoAWSLoadBalancerController \
       --policy-document file:///tmp/lbc-iam-policy.json >/dev/null

eksctl create podidentityassociation --cluster "$CLUSTER" --region "$AWS_REGION" \
  --namespace kube-system --service-account-name aws-load-balancer-controller \
  --permission-policy-arns "$POLICY_ARN" || echo "(association may already exist)"

helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller -n kube-system \
  --set clusterName="$CLUSTER" --set region="$AWS_REGION" --set vpcId="$VPC_ID" \
  --set serviceAccount.create=true --set serviceAccount.name=aws-load-balancer-controller

kubectl -n kube-system rollout status deploy/aws-load-balancer-controller --timeout=180s
kubectl get ingressclass
