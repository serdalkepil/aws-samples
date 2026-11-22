# EKS course demos — Running Containers on Amazon EKS

Files for the instructor demos of the 3-day course. Each demo has a step-by-step script (what to type, what you should see, what to say, cleanup) in its own folder: click the demo ID in the table. The same files are in the course knowledge base under `Running Kubernetes on Amazon EKS/Demos/`.

All commands assume you run them from the `kubernetes/` folder of this repo and have these set:

```bash
export CLUSTER=eks-demo
export AWS_REGION=us-east-1
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export REGISTRY=$ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
```

| Demo | Module | Files used |
|---|---|---|
| [D0](cluster/D0-demo-environment-setup.md) Demo cluster setup (night before) | — | `eks-prerequisites/install-req-AL2023.sh`, `eks-course-demos/cluster/eks-demo-cluster.yaml` |
| [D1](d1-kubectl-contexts/D1-kubectl-with-multiple-clusters.md) kubectl with multiple clusters | M1 | none (kubeconfig commands only) |
| [D2](d2-fargate/D2-working-with-aws-fargate.md) Working with AWS Fargate | M2 | `eks-course-demos/d2-fargate/` |
| [D3](cluster/D3-deploying-a-cluster-with-eksctl.md) Deploying a cluster with eksctl | M3 | `eks-course-demos/cluster/eks-demo-cluster.yaml` |
| [D4](d4-cluster-autoscaler/D4-node-groups-and-cluster-autoscaler.md) Node groups and Cluster Autoscaler | M3 | `eks-course-demos/d4-cluster-autoscaler/` |
| [D5](../eks-simple-nodejs-app/D5-configuring-amazon-ecr.md) Configuring Amazon ECR | M4 | `eks-simple-nodejs-app/` |
| [D6](../eks-helm-nodejs-app/D6-deploying-applications-with-helm.md) Deploying applications with Helm | M4 | `eks-helm-nodejs-app/` |
| [D7](d7-ebs-storage/D7-persistent-storage-with-ebs.md) Persistent storage with EBS | M8 | `eks-course-demos/d7-ebs-storage/` |
| [D8](d8-rbac/D8-rbac-and-access-entries.md) RBAC and access entries | M9 | `eks-course-demos/d8-rbac/` |
| [E1](e1-hpa/E1-hpa-and-node-scale-out.md) HPA and node scale-out | M5 | `eks-course-demos/e1-hpa/`, `eks-course-demos/d4-cluster-autoscaler/inflate.yaml` |
| [E2](e2-network-policy/E2-networkpolicy-default-deny.md) NetworkPolicy default deny | M6 | `eks-course-demos/e2-network-policy/` |
| [E3](e3-observability/E3-container-insights-and-audit-logs.md) Container Insights and audit logs | M7 | `eks-course-demos/e3-observability/` |
| [E4](../eks-pod-identity-test/E4-eks-pod-identity-vs-irsa.md) EKS Pod Identity vs IRSA | M9 | `eks-pod-identity-test/` |
| [E5](e5-load-balancing/E5-load-balancing-nlb-and-alb.md) Load balancing: NLB Service and ALB Ingress | M6 | `eks-course-demos/e5-load-balancing/`, `eks-simple-nginx/`, `eks-nginx-traffic-sample/` |

## What changed in the older samples (2026-11-22)

- `eks-simple-nodejs-app/`: Node 22 LTS image from ECR Public, non-root user, `/healthz` endpoint, version and Pod name on the page; `deployment.yaml` now creates its namespace and a Service, uses `${IMAGE}` instead of a hard-coded account ID, and has requests, limits, and probes.
- `eks-helm-nodejs-app/`: fixed `{{ Release.Name }}` → `{{ .Release.Name }}`; the Service selector now matches the Pods (it pointed at `app: nginx-project`); release-scoped labels; Ingress only when `ingress.enabled` and with `ingressClassName: alb`; no account ID in `values.yaml`; NOTES.txt.
- `eks-simple-nginx/`: ECR Public nginx image, NLB through the AWS Load Balancer Controller (`loadBalancerClass`), resource requests.
- `eks-nginx-traffic-sample/`: moved from the retired ingress-nginx controller to an ALB Ingress; no `{{placeholders}}` left; Services on port 80; Deployments instead of bare Pods.
- `eks-pod-identity-test/`: rewritten demo (no pinned add-on version, no blank account in ARNs), manifest split out into `pod-identity-deployment.yaml`, AWS CLI image.
- `eks-prerequisites/`: kubectl from `dl.k8s.io` (the old Google Storage path is gone), latest Helm release, Docker and `envsubst`; `install-req.sh` marked deprecated (Amazon Linux 2 end of support).
- `helm-eks-amazon-linux-2023.md`: eksctl-io URL, managed node group on AL2023, no archived `stable` repo, no hard-coded account ID.
