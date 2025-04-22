### Create an Amazon EKS Cluster
Y
ou can create an EKS cluster using the AWS Management Console or eksctl.

Using eksctl (recommended)

Create a file named cluster.yaml:

yaml

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

Create the EKS cluster using the configuration file:
powershelleksctl create cluster -f cluster.yaml