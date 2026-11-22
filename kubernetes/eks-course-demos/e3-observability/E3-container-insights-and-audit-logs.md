# E3 — Container Insights and control-plane audit logs (extra, not in the deck)

> Runs from the repo's `kubernetes/` folder (`cd ~/src/aws-samples/kubernetes`). Course copy: knowledge base `Running Kubernetes on Amazon EKS/Demos/`.

| | |
|---|---|
| **Module / slide** | M7 S14–S18 (and M9 for the audit trail) |
| **Time** | 5 minutes live (+10 minutes setup the night before) |
| **Repo** | `eks-course-demos/e3-observability/*.logsinsights` (saved queries) |
| **Needs** | D0 cluster (control-plane logging api/audit/authenticator is on in the cluster config). Run E1 or D8 earlier so there's data. |

## Goal

The managed way to observe EKS: the **CloudWatch Observability add-on** (Container Insights with enhanced observability + Fluent Bit + Application Signals) and **control-plane audit logs** queried with Logs Insights. Good contrast before Lab 4, where students build the do-it-yourself pipeline.

## Step 1 — Night before: install the add-on

```bash
source ~/eks-demo.env
eksctl create podidentityassociation --cluster $CLUSTER --region $AWS_REGION \
  --namespace amazon-cloudwatch --service-account-name cloudwatch-agent \
  --permission-policy-arns arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
aws eks create-addon --cluster-name $CLUSTER --addon-name amazon-cloudwatch-observability
aws eks wait addon-active --cluster-name $CLUSTER --addon-name amazon-cloudwatch-observability
kubectl get pods -n amazon-cloudwatch
# cloudwatch-agent-* and fluent-bit-* on every EC2 node
```

(If the agent Pods log AccessDenied: restart them after the association exists, `kubectl -n amazon-cloudwatch rollout restart ds`. If your add-on version doesn't pick up Pod Identity credentials, the simplest demo fallback is to attach `CloudWatchAgentServerPolicy` to the node role, or pass an IRSA role with `--service-account-role-arn` on `create-addon`.)

Give it 10 minutes before class to fill the dashboards.

## Step 2 — Container Insights tour (2 min)

Console click path:

1. **CloudWatch → Insights → Container Insights**, cluster `eks-demo`.
2. Cluster view: CPU, memory, node count, Pod counts.
3. Switch to **Nodes**, then **Pods**: pick a Pod with restarts (the D5 `/error` Pod if you kept it, or `php-apache` from E1).
4. Open a Pod → **container logs** link (Fluent Bit sent them to `/aws/containerinsights/eks-demo/application`).

**Say:** *"One add-on: metrics from the CloudWatch agent, logs from Fluent Bit. Exactly the S15 diagram, installed and upgraded by EKS."*

## Step 3 — Control-plane audit logs (2 min)

1. **CloudWatch → Logs → Log groups → `/aws/eks/eks-demo/cluster`**. Show the streams: `kube-apiserver-…`, `kube-apiserver-audit-…`, `authenticator-…` (the S18 log types).
2. **Logs Insights**, select that log group, paste `audit-writes.logsinsights`:

```
fields @timestamp, user.username, verb, objectRef.resource, objectRef.namespace, objectRef.name
| filter verb in ["create", "delete", "patch", "update"]
| filter user.username not like /^system:/
| sort @timestamp desc
| limit 25
```

3. Then `who-is-forbidden.logsinsights` (403s): the `EksDemoDev` role's Forbidden calls from D8 show up with the IAM role ARN.

**Say:** *"Who deleted the Deployment at 03:00? This answers it: the IAM identity, the verb, the object. That's why audit + authenticator logs are the security minimum (Module 9)."*

## Step 4 — Bridge to Lab 4

*"In the lab you'll build the other way: Fluent Bit → Firehose → OpenSearch, and Prometheus → Grafana. Same pillars, more control, more to run."*

## Cleanup (end of course, or keep until then)

```bash
aws eks delete-addon --cluster-name $CLUSTER --addon-name amazon-cloudwatch-observability
eksctl delete podidentityassociation --cluster $CLUSTER --region $AWS_REGION \
  --namespace amazon-cloudwatch --service-account-name cloudwatch-agent
# CloudWatch: delete /aws/containerinsights/eks-demo/* log groups
```

## If it breaks

| Symptom | Fix |
|---|---|
| Container Insights shows no cluster | Agent can't write metrics: check the Pod Identity association, restart the DaemonSets |
| No audit stream | Control-plane logging off: `aws eks describe-cluster --name $CLUSTER --query cluster.logging` |
| Logs Insights query returns nothing | Time range too short; set "Last 3 hours" |
