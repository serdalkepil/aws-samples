# Helm Demo with Amazon EKS on Amazon Linux 2023

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

1. Download Helm script and install:
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

2. Verify installation:
   ```bash
   helm version
   ```

### Install eksctl on Amazon Linux 2023

1. Download and extract the latest eksctl release:
   ```bash
   curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
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
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 029916934188.dkr.ecr.eu-west-1.amazonaws.com
```

Note: If you receive an error using the AWS CLI, make sure that you have the latest version of the AWS CLI and Docker installed.

Build your Docker image using the following command. For information on building a Docker file from scratch see the instructions here. You can skip this step if your image is already built. 
After the build completes, tag your image so you can push the image to this repository:
Run the following commands to build and push this image to your newly created AWS repository:

```bash
docker build -t nodejs-simple-app .
docker tag nodejs-simple-app:latest 029916934188.dkr.ecr.eu-west-1.amazonaws.com/nodejs-simple-app:latest
docker push 029916934188.dkr.ecr.eu-west-1.amazonaws.com/nodejs-simple-app:latest
```

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
   
   nodeGroups:
     - name: ng-1
       instanceType: t3.medium
       desiredCapacity: 2
       ssh:
         allow: false
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
   - Kubernetes version: 1.24 or later
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

1. Add the official Helm stable repository:
   ```bash
   helm repo add stable https://charts.helm.sh/stable
   ```

2. Update the Helm repositories:
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

```bash

cd eks-helm-nodejs-app/
mkdir myapp
cd my-app

# check the files and delete templates folder content 
helm create my-app
rm -rf *

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
