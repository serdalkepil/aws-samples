# D7 — Provisioning persistent storage with Amazon EBS

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M8 S30 (instructor notes describe this demo) |
| **Deck status** | Optional. Deck steps: deploy an EBS StorageClass, a PVC, an app using the PVC; confirm PV and app status; remove app and PVC; confirm PV status. Notes: *"Call out the reclaimPolicy setting (Retain)."* |
| **Time** | 10 minutes |
| **Repo** | `eks-course-demos/d7-ebs-storage/ebs-retain.yaml`, `writer-pod.yaml` |
| **Needs** | D0 done (EBS CSI driver add-on running) |

## Goal

StorageClass → PVC → PV → Pod, live. Show `WaitForFirstConsumer` (volume created in the Pod's AZ), data surviving a Pod restart, and `Retain` keeping the EBS volume after the PVC is gone.

## Steps

### 1. The CSI driver is running

```bash
source ~/eks-demo.env
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver
kubectl get csidriver
kubectl get storageclass
```

**Say:** *"The CSI driver is the piece that calls the EC2 API to create and attach volumes (S18). It's an EKS add-on with its own IAM permissions."*

### 2. The StorageClass and PVC

```bash
cat eks-course-demos/d7-ebs-storage/ebs-retain.yaml
kubectl apply -f eks-course-demos/d7-ebs-storage/ebs-retain.yaml
kubectl get sc ebs-retain
kubectl get pvc data-pvc
# STATUS Pending
```

**Ask:** *"Why Pending? Is something broken?"* → `kubectl describe pvc data-pvc` shows `waiting for first consumer to be created before binding`. **Say:** *"EBS lives in one AZ. Kubernetes waits until it knows which node, and so which AZ, the Pod lands on. S15's `Immediate` mode would guess, and could guess wrong."*

### 3. The Pod that uses it

```bash
cat eks-course-demos/d7-ebs-storage/writer-pod.yaml
kubectl apply -f eks-course-demos/d7-ebs-storage/writer-pod.yaml
kubectl wait --for=condition=Ready pod/writer --timeout=120s
kubectl get pvc,pv
# PVC Bound, a PV named pvc-... appeared (dynamically provisioned)
```

### 4. Prove it's a real EBS volume in the node's AZ

```bash
PV=$(kubectl get pvc data-pvc -o jsonpath='{.spec.volumeName}')
VOL=$(kubectl get pv $PV -o jsonpath='{.spec.csi.volumeHandle}')
NODE=$(kubectl get pod writer -o jsonpath='{.spec.nodeName}')
echo "volume $VOL on node $NODE"
aws ec2 describe-volumes --volume-ids $VOL --query 'Volumes[0].{AZ:AvailabilityZone,Type:VolumeType,Size:Size,Encrypted:Encrypted,State:State}'
kubectl get node $NODE -L topology.kubernetes.io/zone
```

Same AZ, gp3, encrypted, `in-use`. Show it in the EC2 console → Volumes too.

### 5. Data outlives the Pod

```bash
kubectl exec writer -- tail -3 /data/out.txt
kubectl delete pod writer
kubectl apply -f eks-course-demos/d7-ebs-storage/writer-pod.yaml
kubectl wait --for=condition=Ready pod/writer --timeout=120s
kubectl exec writer -- head -3 /data/out.txt          # the old lines are still there
```

### 6. (Optional, 1 min) Expand the volume

```bash
kubectl patch pvc data-pvc -p '{"spec":{"resources":{"requests":{"storage":"8Gi"}}}}'
kubectl get pvc data-pvc -w        # CAPACITY 4Gi -> 8Gi (allowVolumeExpansion: true)
```

### 7. Delete the app and the claim: the punchline

```bash
kubectl delete pod writer
kubectl delete pvc data-pvc
kubectl get pv $PV
# STATUS Released, RECLAIM POLICY Retain
aws ec2 describe-volumes --volume-ids $VOL --query 'Volumes[0].State'
# "available": the EBS volume and its data still exist
```

**Say:** *"With `Delete`, the usual default, that volume and the data would be gone right now. `Retain` keeps it, but now a human has to deal with it. Kubernetes won't reuse a Released PV on its own."*

## Bridge to the activity (S31)

*"EBS: one Pod, one AZ, one volume. What if three replicas need the same files, or the app runs on Fargate?"* → EFS (the activity answers).

## Cleanup

```bash
kubectl delete pv $PV
aws ec2 delete-volume --volume-id $VOL      # Retain means Kubernetes won't
kubectl delete sc ebs-retain
```

## If it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| PVC stays Pending after the Pod exists | EBS CSI controller not running or no IAM permissions | `kubectl -n kube-system logs deploy/ebs-csi-controller -c csi-provisioner` |
| Pod `ContainerCreating`, `Multi-Attach error` after step 5 | Old attachment still detaching | Wait 30–60 s |
| On an Auto Mode cluster nothing provisions | Wrong provisioner | Use `ebs.csi.eks.amazonaws.com` in the StorageClass |
