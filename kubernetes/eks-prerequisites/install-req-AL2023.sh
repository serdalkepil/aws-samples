#!/usr/bin/env bash

echo "#####################################################################"
echo "Cloud9 k8s Tools Installation Script for Amazon Linux 2023 #########"
echo "############################################ by #Serdal Kepil########"

# step 1
echo "update and install prerequisites ##############################################"
sudo dnf -y update
sudo dnf groupinstall "Development Tools" -y
sudo dnf install gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel git curl unzip tar -y
echo "update and install prerequisites completed #############################"

# step 2
echo "update python version to 3.11.x (AL2023 default) #########################"
# Amazon Linux 2023 comes with Python 3.9+ by default, but let's ensure we have the latest
sudo dnf install python3 python3-pip python3-devel -y

# If you specifically need Python 3.9.13, uncomment the pyenv section below:
# echo "Installing pyenv for Python 3.9.13 ######################################"
# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# cat << 'EOT' >> ~/.bashrc
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
# EOT
# export PYENV_ROOT="$HOME/.pyenv"
# export PATH="$PYENV_ROOT/bin:$PATH"
# eval "$(pyenv init -)"
# pyenv install 3.9.13
# pyenv global 3.9.13

# For Amazon Linux 2023, use the system Python
python3 --version
echo "python setup completed ################################################"

# step 3
echo "update AWS CLI version to latest ##############################################"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update
rm -rf aws awscliv2.zip
echo "AWS CLI installation completed #########################################"

# step 4
echo "install kubectl ##############################################"
# Get latest stable version
KUBECTL_VERSION=$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)
curl -LO "https://storage.googleapis.com/kubernetes-release/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
kubectl version --client
echo "kubectl installation completed ####################################"

# step 5 - aws-iam-authenticator is deprecated as noted in original script
# AWS CLI v2 includes the necessary authentication functionality

# step 6
echo "install eksctl ##############################################"
# Detect architecture automatically
ARCH=$(uname -m)
case $ARCH in
    x86_64) ARCH="amd64" ;;
    aarch64) ARCH="arm64" ;;
    armv7l) ARCH="armv7" ;;
    armv6l) ARCH="armv6" ;;
esac

PLATFORM=$(uname -s)_$ARCH
echo "Installing eksctl for platform: $PLATFORM"

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

if [ $? -eq 0 ]; then
    echo "Checksum verification passed"
    tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp
    sudo mv /tmp/eksctl /usr/local/bin
    rm -f eksctl_$PLATFORM.tar.gz
    eksctl version
    echo "eksctl installation completed ######################################"
else
    echo "Checksum verification failed! Please check the download."
    exit 1
fi

# step 7 - Additional tools commonly used with Kubernetes
echo "install helm (optional) ###############################################"
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
rm -f get_helm.sh
helm version
echo "helm installation completed #######################################"

# Verify installations
echo "Verifying installations ############################################"
echo "Python version:"
python3 --version
echo "AWS CLI version:"
aws --version
echo "kubectl version:"
kubectl version --client --short 2>/dev/null || kubectl version --client
echo "eksctl version:"
eksctl version
echo "helm version:"
helm version --short

echo "#####################################################################"
echo "Completed all steps for Amazon Linux 2023 ##########################"
echo "############################################ by #Serdal Kepil########"
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials: aws configure"
echo "2. Update kubeconfig: aws eks update-kubeconfig --region <region> --name <cluster-name>"
echo "#####################################################################"