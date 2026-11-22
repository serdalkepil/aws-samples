# E5 — Load balancing: NLB Service and ALB Ingress (extra, not in the deck)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M6 S27–S32 |
| **Time** | 10 minutes live (load balancers take 2–3 minutes each to become active: start them, then talk) |
| **Repo** | `eks-course-demos/e5-load-balancing/install-lbc.sh`, `eks-simple-nginx/nginx-deployment.yaml`, `eks-nginx-traffic-sample/nginx-traffic-sample.yaml` (both updated 2026-11-22) |
| **Needs** | D0 cluster, Helm. Install the AWS Load Balancer Controller the night before (step 1). Not needed on EKS Auto Mode. |

## Goal

The two ways traffic enters the cluster from outside: a **LoadBalancer Service → NLB** (L4, IP targets) and an **Ingress → one ALB with path routing** to two Services (L7). Also why the deck's ingress-nginx option is gone.

## Step 1 — Night before: install the controller

```bash
source ~/eks-demo.env
bash eks-course-demos/e5-load-balancing/install-lbc.sh
kubectl get ingressclass          # alb
kubectl -n kube-system get deploy aws-load-balancer-controller
```

The script creates the IAM policy from the controller's own release, a Pod Identity association for its service account, and installs the Helm chart from `aws.github.io/eks-charts`.

## Step 2 — NLB with a LoadBalancer Service (S27–S29)

```bash
cat eks-simple-nginx/nginx-deployment.yaml
kubectl apply -f eks-simple-nginx/nginx-deployment.yaml
kubectl get svc nginx-project -w        # EXTERNAL-IP fills in with an NLB DNS name
```

**Point out in the YAML:** `loadBalancerClass: service.k8s.aws/nlb` (the deck's S29 misspells it `loadbalancerClass`, which the API ignores), the `internet-facing` scheme annotation (required since controller v2.2, per the S29 notes), and `nlb-target-type: ip` (S28 IP mode: the NLB sends traffic straight to Pod IPs).

While it provisions, EC2 console → Load Balancers → the new NLB → Target groups → **targets are Pod IPs**, not instances.

```bash
NLB=$(kubectl get svc nginx-project -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -s http://$NLB | grep -o '<title>.*</title>'      # DNS may need 1–2 more minutes
kubectl get pods -l app=nginx-project -o wide          # compare IPs with the target group
```

## Step 3 — One ALB, two Services (S30–S32)

```bash
less eks-nginx-traffic-sample/nginx-traffic-sample.yaml
kubectl apply -f eks-nginx-traffic-sample/nginx-traffic-sample.yaml
kubectl -n traffic-demo get ingress fruit -w            # ADDRESS fills in (2–3 min)
```

**Point out:** `ingressClassName: alb`, two path rules, and the backend `port.number: 80`, the **Service port**. The deck's S32 example uses NodePorts 32003/32004 there, which is wrong.

```bash
ALB=$(kubectl -n traffic-demo get ingress fruit -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -s http://$ALB/apple      # apple
curl -s http://$ALB/banana     # banana
curl -s -o /dev/null -w '%{http_code}\n' http://$ALB/cherry   # 404 from the ALB default rule
```

Console: the ALB → Listeners → rules: `/apple*` and `/banana*` → two target groups.

**Say:** *"One load balancer for many Services: that's the reason Ingress exists (S30). On the old version of this sample the controller was ingress-nginx; the Kubernetes project retired it in March 2026, so it gets no security fixes. On EKS use the AWS Load Balancer Controller, and for new designs consider the Gateway API, which the controller supports in GA."*

### Optional: steady traffic for Container Insights / Lab 4

```bash
kubectl -n traffic-demo run traffic-generator --image=curlimages/curl:8.11.1 --restart=Never -- \
  sh -c "while true; do curl -s -o /dev/null http://$ALB/apple; curl -s -o /dev/null http://$ALB/banana; sleep 1; done"
```

## Cleanup (delete Services/Ingresses BEFORE the cluster: load balancers block VPC deletion)

```bash
kubectl delete -f eks-nginx-traffic-sample/nginx-traffic-sample.yaml
kubectl delete -f eks-simple-nginx/nginx-deployment.yaml
# EC2 console: confirm the NLB and ALB are gone (1–2 min)
# End of course:
# helm uninstall aws-load-balancer-controller -n kube-system
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| Service EXTERNAL-IP stays `<pending>` | Controller not running, or `loadBalancerClass` typo | `kubectl -n kube-system logs deploy/aws-load-balancer-controller | tail` |
| Ingress ADDRESS empty, event "couldn't auto-discover subnets" | Public subnets not tagged `kubernetes.io/role/elb=1` | eksctl tags them; check the VPC was created by eksctl |
| Controller logs AccessDenied | Pod Identity association missing or created after the Pod | Re-run the script; `kubectl -n kube-system rollout restart deploy/aws-load-balancer-controller` |
| curl fails right after ADDRESS appears | DNS not propagated yet | Wait 60 s |
