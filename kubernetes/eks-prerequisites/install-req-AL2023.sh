#!/usr/bin/env bash

echo "#####################################################################"
echo "Cloud9 k8s Tools Installation Script for Amazon Linux 2023 #########"
echo "############################################ by #Serdal Kepil########"

# Works both as EC2 user data (cloud-init runs it as root, often with no HOME/USER set)
# and interactively (bash install-req-AL2023.sh). Output in user data: /var/log/cloud-init-output.log
export HOME=${HOME:-/root}
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
# The user who should run docker without sudo: the sudo caller, else ec2-user, else the current user
if [ -n "${SUDO_USER:-}" ]; then TARGET_USER=$SUDO_USER
elif id ec2-user >/dev/null 2>&1; then TARGET_USER=ec2-user
else TARGET_USER=$(id -un); fi
# Download into a scratch folder, not whatever directory cloud-init happens to run in
WORKDIR=$(mktemp -d) && cd "$WORKDIR"

# step 1
echo "update and install prerequisites ##############################################"
sudo dnf -y update
sudo dnf groupinstall "Development Tools" -y
sudo dnf install gcc openssl-devel bzip2-devel libffi-devel zlib-devel xz-devel git unzip tar -y   # curl-minimal is preinstalled; installing curl would conflict
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
curl "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o "awscliv2.zip"
unzip -q -o awscliv2.zip      # -o: never stop to ask about overwriting (re-runs)
sudo ./aws/install --update
rm -rf aws awscliv2.zip
echo "AWS CLI installation completed #########################################"

# step 4
echo "install kubectl ##############################################"
# Match kubectl to your cluster (within one minor version). Override with: KUBECTL_VERSION=v1.35.0 ./install-req-AL2023.sh
# (storage.googleapis.com/kubernetes-release is no longer the download location; dl.k8s.io is.)
KARCH=$(uname -m); [ "$KARCH" = "aarch64" ] && KARCH=arm64 || KARCH=amd64
KUBECTL_VERSION=${KUBECTL_VERSION:-$(curl -sL https://dl.k8s.io/release/stable.txt)}
curl -sLO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KARCH}/kubectl"
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

# Verify checksum. Match the exact file name: the checksums file also lists
# eksctl_<platform>.tar.gz.sbom.json, which we don't download (grep $PLATFORM alone matched both lines).
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" \
  | grep " eksctl_${PLATFORM}.tar.gz$" | sha256sum --check

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
echo "install helm ###############################################"
# Installs the latest Helm release (Helm 4 since Nov 2025; Helm 3 gets security fixes only until Feb 2027).
# Pin a version with: HELM_VERSION=v4.x.y ./install-req-AL2023.sh
HELM_VERSION=${HELM_VERSION:-$(curl -s https://api.github.com/repos/helm/helm/releases/latest | grep '"tag_name"' | cut -d '"' -f4)}
if [ -z "$HELM_VERSION" ]; then
    echo "Couldn't read the latest Helm version from the GitHub API (rate limit?). Set HELM_VERSION=v4.x.y and re-run."
    exit 1
fi
curl -fsSL -o helm.tar.gz "https://get.helm.sh/helm-${HELM_VERSION}-linux-${KARCH}.tar.gz"
tar -xzf helm.tar.gz -C /tmp && sudo mv /tmp/linux-${KARCH}/helm /usr/local/bin/helm
rm -rf helm.tar.gz /tmp/linux-${KARCH}
helm version
echo "helm installation completed #######################################"

# step 8 - Docker (for building and pushing images in the ECR demo) and envsubst (for manifests)
echo "install docker and gettext ###########################################"
sudo dnf install -y docker gettext
sudo systemctl enable --now docker
sudo usermod -aG docker "$TARGET_USER"   # takes effect at next login (or: newgrp docker)
echo "Added $TARGET_USER to the docker group"
echo "docker installation completed #####################################"

# Verify installations
echo "Verifying installations ############################################"
echo "Python version:"
python3 --version
echo "AWS CLI version:"
aws --version
echo "kubectl version:"
kubectl version --client
echo "eksctl version:"
eksctl version
echo "helm version:"
helm version --short
echo "docker version:"
docker --version

cd / && rm -rf "$WORKDIR"

echo "#####################################################################"
echo "Completed all steps for Amazon Linux 2023 ##########################"
echo "############################################ by #Serdal Kepil########"
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials: aws configure"
echo "2. Update kubeconfig: aws eks update-kubeconfig --region <region> --name <cluster-name>"
echo "#####################################################################"