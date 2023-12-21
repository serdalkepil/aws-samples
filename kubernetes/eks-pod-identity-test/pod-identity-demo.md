# Pod Identity Demo

## Intro

AWS EKS has introduced a new enhanced mechanism called Pod Identity Association for cluster administrators to configure Kubernetes applications to receive IAM permissions required to connect with AWS services outside of the cluster. Pod Identity Association leverages IRSA however, it makes it configurable directly through EKS API, eliminating the need for using IAM API altogether.

As a result, IAM roles no longer need to reference an OIDC provider and hence won't be tied to a single cluster anymore. This means, IAM roles can now be used across multiple EKS clusters without the need to update the role trust policy each time a new cluster is created. This in turn, eliminates the need for role duplication and simplifies the process of automating IRSA altogether.

### EKS Pod Identity Restrictions

- Since we will be using new APIs, you will need to update aws-cli to the latest version.
- These are the compatible EKS Pod Identity cluster versions.
- Worker nodes in the cluster have to be Linux Amazon EC2 instances. Fargate and pods that run on Windows Amazon EC2 instances aren’t supported.

## Create IAM Role

Create an IAM role with following trust policy

pod-idenity-s3-example

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "pods.eks.amazonaws.com"
            },
            "Action": [
                "sts:AssumeRole",
                "sts:TagSession"
            ]
        }
    ]
}
```

Attach AmazonS3ReadOnlyAccess permission.

## Install EKS Pod Identity Agent Add-on to EKS Cluster

You can use web console or following command to install  EKS Pod Identity Agent

```shell
aws eks create-addon \
  --cluster-name my-cluster \
  --addon-name eks-pod-identity-agent \
  --addon-version v1.0.0-eksbuild.1
```

! You need to use latest version of AWS-CLI

Once the addon is installed, you can see the new DaemonSet running in EKS:

`kubectl get pods -n kube-system`

## Pod Identity Associations

Use the new AWS API create-pod-identity-association to attach our IAM role to an EKS service account and namespace:

```sh
aws eks create-pod-identity-association \
  --cluster-name your-cluster \
  --service-account pod-identity \
  --role-arn arn:aws:iam:::role/pod-idenity-s3-example \
  --namespace default

aws eks list-pod-identity-associations --cluster-name your-cluster
```

## Spin up a Test Pod

Create and apply your k8s manifest file as follows.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pod-identity
  labels:
    app: pod-identity
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pod-identity
  template:
    metadata:
      labels:
        app: pod-identity
    spec:
      serviceAccountName: pod-identity
      containers:
      - name: pod-identity
        image: makoreactor/debug:latest
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-identity
  labels:
    app: pod-identity
```

`kubectl apply -f depployment.yaml`


## Test it

Check the local generated credentials

```sh
kubectl get pods
kubectl exec -ti pod-identity-6798cdbd9d-drswx -- bash
env | sort
cat $AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE
SERVICE_TOKEN=`cat /var/run/secrets/pods.eks.amazonaws.com/serviceaccount/eks-pod-identity-token` 
curl 169.254.170.23/v1/credentials -H "Authorization: $SERVICE_TOKEN"

You can use with CLI if you configure env. auth. vars

```sh
export AWS_ACCESS_KEY_ID=ASI...
export AWS_SECRET_ACCESS_KEY=Kmfg...
export AWS_SESSION_TOKEN="IQoJb3..." 
aws sts get-caller-identity
```

## Delete Created Resources

Delete created resources and addon

```sh
kubectl delete deployment pod-identity
aws eks delete-pod-identity-association --cluster-name eks-cluster --association-id a-kvbxt9pyavos3iwxy
kubectl delete sa pod-identity
aws eks delete-addon --cluster-name eks-cluster --addon-name eks-pod-identity-agent
```
