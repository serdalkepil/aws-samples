# D5 — Configuring Amazon ECR

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M4 S11–S12 (S12 is the hidden demo slide) |
| **Deck status** | Optional. Deck steps: create a repository, authenticate Docker, build and tag, push, consume the image. |
| **Time** | 8 minutes (image pre-built in D0 step 5) |
| **Repo** | `eks-simple-nodejs-app/` (Express app + Dockerfile + `deployment.yaml`) |
| **Needs** | D0 done, Docker running |

## Goal

The registry workflow from S8, end to end, ending with the image running on EKS. Also: tag immutability, scan on push (AWS native basic scanning, not Clair), and no imagePullSecret.

## Steps

### 1. The app and its Dockerfile

```bash
source ~/eks-demo.env
cat eks-simple-nodejs-app/simple-nodejs-app/app.js | head -20
cat eks-simple-nodejs-app/simple-nodejs-app/Dockerfile
```

**Point out:** base image from **ECR Public** (no Docker Hub rate limits), runs as non-root `node`, `/healthz` for probes, `/error` to crash on purpose (useful later).

### 2. Create the repository (already done in D0: show it)

```bash
aws ecr describe-repositories --repository-names nodejs-simple-app \
  --query 'repositories[0].{uri:repositoryUri,immutable:imageTagMutability,scanOnPush:imageScanningConfiguration.scanOnPush}'
```

If it doesn't exist:

```bash
aws ecr create-repository --repository-name nodejs-simple-app \
  --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
```

**Say:** *"One private registry per account and Region, many repositories inside it. That's KC1 for this module."*

### 3. Authenticate Docker to the registry

```bash
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY
# Login Succeeded
```

**Say:** *"The password is a 12-hour token from IAM. No long-lived registry password anywhere."*

### 4. Build and tag

```bash
cd eks-simple-nodejs-app/simple-nodejs-app
docker build -t nodejs-simple-app:1.0 .             # Apple silicon: --platform linux/amd64
docker tag nodejs-simple-app:1.0 $REGISTRY/nodejs-simple-app:1.0
docker images | grep nodejs-simple-app
cd ~/src/aws-samples/kubernetes
```

### 5. Push and look at the scan

```bash
docker push $REGISTRY/nodejs-simple-app:1.0
aws ecr wait image-scan-complete --repository-name nodejs-simple-app --image-id imageTag=1.0
aws ecr describe-image-scan-findings --repository-name nodejs-simple-app --image-id imageTag=1.0 \
  --query 'imageScanFindings.findingSeverityCounts'
```

Console: ECR → `nodejs-simple-app` → image `1.0` → vulnerabilities.

**Say:** *"Basic scanning is AWS native now; S11 still says Clair, which AWS retired in February 2026. Enhanced scanning adds language packages and continuous rescans through Amazon Inspector."*

### 6. Immutable tags in action

```bash
docker push $REGISTRY/nodejs-simple-app:1.0
# ... tag invalid: The image tag '1.0' already exists ... cannot be overwritten because the repository is immutable
```

**Say:** *"Nobody can move `1.0` to different code behind your back. Never deploy `latest`."*

### 7. Consume it from EKS

```bash
export IMAGE=$REGISTRY/nodejs-simple-app:1.0
envsubst < eks-simple-nodejs-app/deployment.yaml | kubectl apply -f -
kubectl -n eks-nodejs-app rollout status deploy/eks-nodejs-deployment
kubectl -n eks-nodejs-app get pods -o wide
```

**Ask:** *"Where's the imagePullSecret?"* (None needed: the node IAM role has ECR read access, D4 step A2.)

### 8. See it, and see self-healing

```bash
kubectl -n eks-nodejs-app port-forward svc/eks-nodejs-service 8080:80
```

Open http://localhost:8080 and refresh a few times: the Pod name changes (port-forward pins one Pod per connection; open a new browser tab or use curl in a loop to show different Pods). Then open http://localhost:8080/error, and in another terminal:

```bash
kubectl -n eks-nodejs-app get pods -w      # RESTARTS goes 0 -> 1 on one Pod
```

**Say:** *"The container died, the kubelet restarted it. That's the control loop from Module 1."* (Restart port-forward if it dropped.)

## Bridge to Helm

*"Three replicas, one image, one YAML file with an environment variable substituted in. What happens when you have twenty services and three environments? That's Helm, next."*

## Cleanup

```bash
kubectl delete namespace eks-nodejs-app
# Keep the repository and image for D6.
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| `no basic auth credentials` on push | Docker login expired or for another Region | Repeat step 3 |
| `ImagePullBackOff`, `exec format error` in logs | Built arm64 image on a Mac, nodes are amd64 | Rebuild with `--platform linux/amd64` and push as `1.1` (1.0 is immutable) |
| `ImagePullBackOff`, `not found` | `$IMAGE` not set when you ran envsubst | `kubectl -n eks-nodejs-app get deploy -o jsonpath='{..image}'` |
| Scan shows nothing | Scan still running | Wait for `image-scan-complete` |
