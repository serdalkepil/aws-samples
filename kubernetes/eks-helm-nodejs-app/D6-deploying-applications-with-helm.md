# D6 — Deploying applications with Helm

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M4 S20–S21 (S21 is the hidden demo slide) |
| **Deck status** | Optional. Deck steps: install an application, upgrade it, build a new chart, deploy a chart. Notes: *"Helm is not magic — do a Helm dry run and you can see what it's doing."* |
| **Time** | 10–12 minutes |
| **Repo** | `eks-helm-nodejs-app/` (chart, fixed 2026-11), the image from D5 |
| **Needs** | D5 done (image `nodejs-simple-app:1.0` in ECR), Helm installed |

## Goal

Install a public chart and roll it back, then deploy your own chart: template, dry run, install, upgrade, history, rollback, package, push to ECR as an OCI artifact.

## Part A — Install and upgrade an existing chart (Fluent Bit from the AWS EKS charts repo)

### A1. Add the repo and find the chart

```bash
source ~/eks-demo.env
helm repo add eks https://aws.github.io/eks-charts
helm repo update eks
helm search repo eks/aws-for-fluent-bit
```

**Say:** *"Artifact Hub lists repos like this one. Helm downloads the chart, renders the templates, sends YAML to the API server. That's all."*

### A2. Install, then look at what it created

```bash
helm install aws-for-fluent-bit eks/aws-for-fluent-bit -n kube-system
helm ls -n kube-system
kubectl get daemonset -n kube-system aws-for-fluent-bit     # one Pod per EC2 node (M1 DaemonSet)
```

### A3. Upgrade and roll back

```bash
helm upgrade aws-for-fluent-bit eks/aws-for-fluent-bit -n kube-system --set cloudWatchLogs.enabled=false
helm history aws-for-fluent-bit -n kube-system                 # revision 1 and 2
helm rollback aws-for-fluent-bit 1 -n kube-system --dry-run
helm rollback aws-for-fluent-bit 1 -n kube-system
helm history aws-for-fluent-bit -n kube-system                 # revision 3 = copy of 1
```

**Say:** *"Rollback doesn't go back in time; it creates a new revision with the old settings."*

(No `cloudWatchLogs` value in your chart version? Use any value from `helm show values eks/aws-for-fluent-bit`; the point is the revision history.)

## Part B — Our own chart

### B1. Anatomy (S18)

```bash
cd eks-helm-nodejs-app
ls -R
cat Chart.yaml            # the mandatory file (KC2): name, version (chart) vs appVersion (app)
cat values.yaml           # defaults; no account ID in here
head -35 templates/deployment.yaml
```

**Point out (S19):** `{{ .Release.Name }}`, `{{ .Values.replicaCount }}`, `{{ .Values.image.tag | default .Chart.AppVersion }}`, the `required` check on `image.repository`, and `include "nodejs.selectorLabels"` from `_helpers.tpl`.

### B2. "Not magic": render locally

```bash
helm lint . --set image.repository=$REGISTRY/nodejs-simple-app
helm template web . --set image.repository=$REGISTRY/nodejs-simple-app | less
```

Then show a failure on purpose:

```bash
helm template web .
# Error: ... Set image.repository to your ECR repository
```

**Say:** *"Helm told us what was missing before anything touched the cluster."*

### B3. Dry run against the cluster, then install

```bash
helm install web . -n demo --create-namespace --set image.repository=$REGISTRY/nodejs-simple-app --dry-run --debug | tail -40
helm install web . -n demo --set image.repository=$REGISTRY/nodejs-simple-app --create-namespace
helm ls -n demo
kubectl -n demo get deploy,svc,pods
```

The NOTES.txt output tells you how to reach it:

```bash
kubectl -n demo port-forward svc/web 8080:80      # http://localhost:8080 shows "Version: 1.0"
```

### B4. Upgrade by changing values, not files

```bash
helm upgrade web . -n demo --reuse-values --set app.version=2.0 --set app.color='#e0007a' --set replicaCount=4
kubectl -n demo rollout status deploy/web
```

Refresh the page (restart port-forward if it dropped): new version and colour. Then:

```bash
helm history web -n demo
helm get values web -n demo        # what you overrode
helm rollback web 1 -n demo        # back to 1.0 / 3 replicas
```

### B5. Two releases of the same chart

```bash
helm install web2 . -n demo --set image.repository=$REGISTRY/nodejs-simple-app --set app.version=blue
kubectl -n demo get pods -L app.kubernetes.io/instance
kubectl -n demo get endpoints web web2
```

**Say:** *"Each Service only selects its own release's Pods, because the labels include the release name. The old version of this chart selected `app: nginx-project`: a Service with no endpoints. The most common Helm bug."*

### B6. Package and publish to ECR as an OCI artifact (S20)

```bash
helm package .                                       # eks-nodejs-helm-app-0.2.0.tgz
aws ecr create-repository --repository-name eks-nodejs-helm-app >/dev/null 2>&1 || true
aws ecr get-login-password --region $AWS_REGION | helm registry login --username AWS --password-stdin $REGISTRY
helm push eks-nodejs-helm-app-0.2.0.tgz oci://$REGISTRY/
helm show chart oci://$REGISTRY/eks-nodejs-helm-app --version 0.2.0
cd ~/src/aws-samples/kubernetes
```

**Bridge to Lab 2:** *"Same chart, different home. In the lab you'll use S3 as the repository: an `index.yaml` plus `.tgz` files. ECR is the AWS-native option today."*

## Cleanup

```bash
helm uninstall web web2 -n demo && kubectl delete namespace demo
helm uninstall aws-for-fluent-bit -n kube-system
rm -f eks-helm-nodejs-app/eks-nodejs-helm-app-*.tgz
```

## If it breaks

| Symptom | Fix |
|---|---|
| `Error: INSTALLATION FAILED: cannot re-use a name that is still in use` | `helm ls -A`; uninstall the old release or use another name |
| Pods `ImagePullBackOff` | Wrong repository or tag: `helm get values web -n demo`; the tag defaults to `appVersion` (1.0) |
| `helm push` → 401 | `helm registry login` expired or wrong Region |
| Old Helm 3 vs Helm 4 output differences | Harmless for this demo |
