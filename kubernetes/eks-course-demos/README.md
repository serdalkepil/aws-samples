# EKS course demos — Running Containers on Amazon EKS

Files for the instructor demos of the 3-day course. The step-by-step scripts (what to type, what to say, what you should see) live in the course knowledge base: `03-Knowledge-Base/AWS_Trainings/Running Kubernetes on Amazon EKS/Demos/`. Each demo file there points back to the paths below.

All commands assume you run them from the `kubernetes/` folder of this repo and have these set:

```bash
export CLUSTER=eks-demo
export AWS_REGION=us-east-1
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export REGISTRY=$ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
```

| Demo | Module | Files used |
|---|---|---|
| D0 Demo cluster setup (night before) | — | `eks-prerequisites/install-req-AL2023.sh`, `eks-course-demos/cluster/eks-demo-cluster.yaml` |
| D1 kubectl with multiple clusters | M1 | none (kubeconfig commands only) |
| D2 Working with AWS Fargate | M2 | `eks-course-demos/d2-fargate/` |
| D3 Deploying a cluster with eksctl | M3 | `eks-course-demos/cluster/eks-demo-cluster.yaml` |
| D4 Node groups and Cluster Autoscaler | M3 | `eks-course-demos/d4-cluster-autoscaler/` |
| D5 Configuring Amazon ECR | M4 | `eks-simple-nodejs-app/` |
| D6 Deploying applications with Helm | M4 | `eks-helm-nodejs-app/` |
| D7 Persistent storage with EBS | M8 | `eks-course-demos/d7-ebs-storage/` |
| D8 RBAC and access entries | M9 | `eks-course-demos/d8-rbac/` |
| E1 HPA and node scale-out | M5 | `eks-course-demos/e1-hpa/`, `eks-course-demos/d4-cluster-autoscaler/inflate.yaml` |
| E2 NetworkPolicy default deny | M6 | `eks-course-demos/e2-network-policy/` |
| E3 Container Insights and audit logs | M7 | `eks-course-demos/e3-observability/` |
| E4 EKS Pod Identity vs IRSA | M9 | `eks-pod-identity-test/` |
| E5 Load balancing: NLB Service and ALB Ingress | M6 | `eks-course-demos/e5-load-balancing/`, `eks-simple-nginx/`, `eks-nginx-traffic-sample/` |

## What changed in the older samples (2026-11-22)

- `eks-simple-nodejs-app/`: Node 22 LTS image from ECR Public, non-root user, `/healthz` endpoint, version and Pod name on the page; `deployment.yaml` now creates its namespace and a Service, uses `${IMAGE}` instead of a hard-coded account ID, and has requests, limits, and probes.
- `eks-helm-nodejs-app/`: fixed `{{ Release.Name }}` → `{{ .Release.Name }}`; the Service selector now matches the Pods (it pointed at `app: nginx-project`); release-scoped labels; Ingress only when `ingress.enabled` and with `ingressClassName: alb`; no account ID in `values.yaml`; NOTES.txt.
- `eks-simple-nginx/`: ECR Public nginx image, NLB through the AWS Load Balancer Controller (`loadBalancerClass`), resource requests.
- `eks-nginx-traffic-sample/`: moved from the retired ingress-nginx controller to an ALB Ingress; no `{{placeholders}}` left; Services on port 80; Deployments instead of bare Pods.
- `eks-pod-identity-test/`: rewritten demo (no pinned add-on version, no blank account in ARNs), manifest split out into `pod-identity-deployment.yaml`, AWS CLI image.
- `eks-prerequisites/`: kubectl from `dl.k8s.io` (the old Google Storage path is gone), latest Helm release, Docker and `envsubst`; `install-req.sh` marked deprecated (Amazon Linux 2 end of support).
- `helm-eks-amazon-linux-2023.md`: eksctl-io URL, managed node group on AL2023, no archived `stable` repo, no hard-coded account ID.
