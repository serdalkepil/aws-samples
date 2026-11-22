# Helm Demo with Amazon EKS on Amazon Linux 2023

> **Updated 2026-11-22.** Tool install URLs, the cluster config, and the image commands are current. For the classroom version of this demo (Module 4, Demo D6), use the step-by-step file `D6 - Deploying applications with Helm.md` in the course's `Demos/` folder; it uses the fixed chart in `eks-helm-nodejs-app/`.

This guide will walk you through setting up Amazon EKS (Elastic Kubernetes Service) on Amazon Linux 2023 and deploying an application using Helm charts.

## Prerequisites

- Amazon Linux 2023 instance
- AWS account with appropriate permissions
- Sufficient permissions to install software and modify system settings

## Step 1: Install Required Tools

### Install AWS CLI on Amazon Linux 2023

1. Update your system packages:
   ```bash
   sudo dnf update -y
   ```

2. Install AWS CLI:
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

3. Verify installation:
   ```bash
   aws --version
   ```

4. Configure AWS CLI:
   ```bash
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, default region, and output format.

### Install kubectl on Amazon Linux 2023

1. Download kubectl:
   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

2. Make kubectl executable and move it to a directory in your PATH:
   ```bash
   chmod +x kubectl
   sudo mv kubectl /usr/local/bin/
   ```

3. Verify installation:
   ```bash
   kubectl version --client
   ```

### Install Helm on Amazon Linux 2023

1. Install the latest Helm release (Helm 4; charts from Helm 3 keep working):
   ```bash
   HELM_VERSION=$(curl -s https://api.github.com/repos/helm/helm/releases/latest | grep '"tag_name"' | cut -d '"' -f4)
   curl -fsSL -o helm.tar.gz "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz"
   tar -xzf helm.tar.gz -C /tmp && sudo mv /tmp/linux-amd64/helm /usr/local/bin/helm
   ```

2. Verify installation:
   ```bash
   helm version
   ```

### Install eksctl on Amazon Linux 2023

1. Download and extract the latest eksctl release:
   ```bash
   curl --silent --location "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
   ```

2. Move the extracted binary to /usr/local/bin:
   ```bash
   sudo mv /tmp/eksctl /usr/local/bin
   ```

3. Verify installation:
   ```bash
   eksctl version
   ```

### Set up ECR and Build & Push the Image

Make sure that you have the latest version of the AWS CLI and Docker installed. For more information, see Getting Started with Amazon ECR. Use the following steps to authenticate and push an image to your repository. For additional registry authentication methods, including the Amazon ECR credential helper, see Registry Authentication .

Retrieve an authentication token and authenticate your Docker client to your registry. Use the AWS CLI:

```bash
export AWS_REGION=eu-west-1
export ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
export REGISTRY=$ACCOUNT.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr create-repository --repository-name nodejs-simple-app --image-scanning-configuration scanOnPush=true 2>/dev/null || true
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $REGISTRY
```

Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here. You can skip this step if your image is already built. 
After the build completes, tag your image so you can push the image to this repository:
Run the following commands to build and push this image to your newly created AWS repository:

```bash
cd eks-simple-nodejs-app/simple-nodejs-app
docker build -t nodejs-simple-app:1.0 .          # on Apple silicon add --platform linux/amd64
docker tag nodejs-simple-app:1.0 $REGISTRY/nodejs-simple-app:1.0
docker push $REGISTRY/nodejs-simple-app:1.0
```

Use a version tag, not `latest`: the cluster then pulls exactly what you pushed.

## Step 2: Create an Amazon EKS Cluster

You can create an EKS cluster using the AWS Management Console or eksctl.

### Using eksctl (recommended)

1. Create a file named `cluster.yaml`:
   ```bash
   cat > cluster.yaml << EOF
   apiVersion: eksctl.io/v1alpha5
   kind: ClusterConfig
   
   metadata:
     name: my-eks-cluster
     region: us-west-2
     version: "1.35"
   
   managedNodeGroups:
     - name: ng-1
       instanceType: t3.medium
       amiFamily: AmazonLinux2023
       desiredCapacity: 2
       privateNetworking: true
   EOF
   ```

2. Create the EKS cluster using the configuration file:
   ```bash
   eksctl create cluster -f cluster.yaml
   ```

   This process will take approximately 15-20 minutes.

### Using AWS Management Console

1. Open the Amazon EKS console at https://console.aws.amazon.com/eks
2. Choose "Create cluster"
3. Fill in the required fields:
   - Name: my-eks-cluster
   - Kubernetes version: the newest one offered (1.34 or later are in standard support as of Nov 2026)
   - Role: Create a new role or use an existing one
   - VPC: Create a new VPC or use an existing one
   - Subnets: Select subnets in at least two Availability Zones
   - Security groups: Create a new security group or use an existing one
4. Choose "Next"
5. Configure the worker nodes:
   - Node group name: my-node-group
   - Node IAM role: Create a new role or use an existing one
   - Instance type: t3.medium
   - Desired capacity: 2
   - Minimum size: 1
   - Maximum size: 4
6. Choose "Next"
7. Review the configuration and choose "Create"

## Step 3: Connect to Your EKS Cluster

1. Update your kubeconfig file:
   ```bash
   aws eks update-kubeconfig --region us-west-2 --name my-eks-cluster
   ```

2. Verify the connection:
   ```bash
   kubectl get nodes
   ```

## Step 4: Set Up Helm

The old `stable` repository (`charts.helm.sh/stable`) is archived; don't add it. Find charts on Artifact Hub (https://artifacthub.io) and add the project's own repo, for example the AWS EKS charts in Step 6. Then:

   ```bash
   helm repo update
   ```

## Step 5: Deploy a Sample Application with Helm

Let's deploy a sample Nginx application using Helm:

1. Create a Helm chart for our application:
   ```bash
   helm create my-nginx-app
   ```

2. Navigate to the chart directory:
   ```bash
   cd my-nginx-app
   ```

3. Review and modify the `values.yaml` file according to your requirements:
   ```bash
   # Edit values.yaml to configure your Nginx deployment
   nano values.yaml
   ```

4. Install the chart:
   ```bash
   helm install my-release ./my-nginx-app
   ```

5. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

## Step 6: Use an Existing Helm Chart

Let's deploy a more complex application using an existing Helm chart from a repository:

FluentBit

   ```bash
      helm version
      helm repo list

      # aws eks team public repo
      helm repo add eks https://aws.github.io/eks-charts

      # find the package
      helm search repo eks fluent

      # install the fluent-bit
      helm install aws-for-fluent-bit --namespace kube-system eks/aws-for-fluent-bit

      # check pods
      kubectl get pods -n kube-system

      # helm check
      helm ls --namespace kube-system

      # check daemonset
      kubectl get daemonset -n kube-system

      # upgrade the deployment
      helm upgrade aws-for-fluent-bit -n kube-system eks/aws-for-fluent-bit 

      # rollback with dry-run
      helm rollback aws-for-fluent-bit 1 -n kube-system --dry-run 

      # rollback without dry-run
      helm rollback aws-for-fluent-bit 1 -n kube-system
   ```

Custom App

The fixed chart is in `eks-helm-nodejs-app/` (release-scoped labels, Service selector that matches the Pods, probes, optional ALB Ingress). To build one from scratch the way the original demo did:

```bash

mkdir -p /tmp/helm-scratch && cd /tmp/helm-scratch

# generate a starter chart, then empty its templates so you write them yourself
helm create my-app
cd my-app
rm -rf templates/*

# under my-app directory, try to install my-app chart
helm install --debug --dry-run myreleasedapp .

# open templates/deployment.yaml
# change name value with the release name placeholder -  name: {{ .Release.Name }}
# after the error try with a different option 
helm install --debug --dry-run myreleasedapp2 .

helm install --debug --dry-run myreleasedapp .

helm install myreleasedapp .

kubectl get deploy

helm ls

helm upgrade myreleasedapp .

helm rollback myreleasedapp 1 

# update version from chart.yaml

helm upgrade myreleasedapp .

helm ls

helm delete myreleasedapp

```

## Step 7: Manage Your Helm Releases

### List Helm Releases

```bash
helm list
```

### Upgrade a Release

```bash
helm upgrade my-release ./my-nginx-app
```

### Rollback a Release

```bash
helm rollback my-release 1
```

### Uninstall a Release

```bash
helm uninstall my-release
```

## Step 8: Clean Up

When you're done with your EKS cluster, remember to delete it to avoid unnecessary costs:

```bash
eksctl delete cluster --name my-eks-cluster --region us-west-2
```

## Troubleshooting

### Common Issues

1. **Connection issues**: 
   - Ensure your AWS credentials are correctly configured
   - Check if your IAM user has the necessary permissions
   - Verify your VPC and subnet configurations

2. **Deployment failures**:
   - Check the pods status: `kubectl get pods`
   - View pod logs: `kubectl logs <pod-name>`
   - Describe the pod: `kubectl describe pod <pod-name>`

3. **Helm chart issues**:
   - Validate your chart: `helm lint ./my-chart`
   - Debug installation: `helm install --debug --dry-run my-release ./my-chart`

## Additional Resources

- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Helm Documentation](https://helm.sh/docs/)
- [kubectl Command Reference](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Conclusion

You've successfully set up Amazon EKS on Amazon Linux 2023 and deployed applications using Helm charts. You've learned how to:

- Install the necessary tools on Amazon Linux 2023
- Create an Amazon EKS cluster
- Connect to your cluster
- Deploy applications using both custom and existing Helm charts
- Manage your Helm releases
- Clean up your resources
