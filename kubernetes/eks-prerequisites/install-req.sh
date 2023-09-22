#!/usr/bin/env bash

echo "#####################################################################"
echo "Cloud9 k8s Tools Installation Script ################################"
echo "############################################ by #Serdal Kepil########"

# step 1
echo "update and install prerequisites ##############################################"
yum -y update
yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel -y
echo "update and install prerequisites ##############################################"

# step 2
echo "update python version to 3.9.13 ##############################################"
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
cat << 'EOT' >> ~/.bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
EOT
source ~/.bashrc
pyenv install 3.9.13
pyenv global 3.9.13
echo "~/.bash_profile".
export PATH="$HOME/.pyenv/shims:$PATH"
source ~/.bash_profile
python --version
echo "update python version is done ##############################################"

# step 3
echo "update AWS CLI version to latest ##############################################"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
echo "update AWS CLI version to latest is done ##############################################"

# step 4
echo "install kubectl ##############################################"
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
echo "install kubectl is done ##############################################"

# step 5 aws-iam-authenticator is deprecated. If you're running the AWS CLI version 1.16.156 or later,
#then you don't need to install the authenticator. Instead, you can use the aws eks get-token command.
#For more information, see Create kubeconfig file manually.

# echo "install aws-iam-authenticator ##############################################"
# curl -o aws-iam-authenticator https://amazon-eks.s3-us-west-2.amazonaws.com/1.12.7/2019-03-27/bin/linux/amd64/aws-iam-authenticator
# chmod +x ./aws-iam-authenticator
# mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$HOME/bin:$PATH
# rm -f aws-iam-authenticator
# echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc
# echo "install aws-iam-authenticator is done ##############################################"

# step 6
echo "install eksctl ##############################################"
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"
# Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check
tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm -f eksctl_$PLATFORM.tar.gz
sudo mv /tmp/eksctl /usr/local/bin
echo "install eksctl is done ##############################################"

echo "#####################################################################"
echo "Completed all steps #################################################"
echo "############################################ by #Serdal Kepil########"