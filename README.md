# AWS Samples Repository by Serdal Kepil

Comprehensive collection of AWS examples, tutorials, and best practices for cloud development and deployment.

## 📁 Repository Structure

### 🏗️ Infrastructure as Code

#### [CDK (Cloud Development Kit)](./cdk/)
- **[demo-app](./cdk/demo-app/)** - Basic CDK application with Lambda integration
- **[rds](./cdk/rds/)** - RDS MySQL database deployment
- **[rekognition-lambda-s3-trigger](./cdk/rekognition-lambda-s3-trigger/)** - Image recognition with S3 triggers
- **[s3-kms-cross-account-replication](./cdk/s3-kms-cross-account-replication/)** - Cross-account S3 replication with KMS
- **[vpc-ec2-rds](./cdk/vpc-ec2-rds/)** - Complete VPC setup with EC2 and RDS
- **[CDK Resources](./cdk/CDK-resources.md)** - Learning resources and documentation

#### [CloudFormation](./cloudformation/)
- EC2 web server templates with cfn-init
- VPC networking with RDS and NAT instances
- Infrastructure automation templates

#### [SAM (Serverless Application Model)](./sam/)
- **[apigtw-lambda-dynamodb-crud](./sam/apigtw-lambda-dynamodb-crud/)** - Complete CRUD API
- **[cognitoJWTValidator](./sam/cognitoJWTValidator/)** - JWT validation with Cognito
- **[java-crud-api-with-layer](./sam/java-crud-api-with-layer/)** - Java-based serverless API with layers

### ☁️ Compute Services

#### [Lambda Functions](./lambda/)
- **[presignedURLFunction](./lambda/presignedURLFunction/)** - S3 presigned URL generation
- **[s3Select](./lambda/s3Select/)** - S3 Select query operations
- **[lambda-url-health-check-service](./lambda-url-health-check-service/)** - Health monitoring service

#### [EC2](./ec2/)
- On-demand vs Spot instances comparison and demos

#### [Elastic Beanstalk](./eb/)
- **[html-website](./eb/html-website/)** - Static website deployment
- **[EB CLI Commands Reference](./eb/README.md)** - Complete CLI documentation

### 🗄️ Storage & Database

#### [S3 (Simple Storage Service)](./s3/)
- **[s3-sdk](./s3/s3-sdk/)** - Python and Node.js SDK examples
- **[static-web-site](./s3/static-web-site/)** - Static website hosting
- Bucket creation and management scripts

#### [DynamoDB](./dynamodb/)
- **[import-csv-with-lambda](./dynamodb/import-csv-with-lambda/)** - CSV data import automation

### 🤖 AI/ML & GenAI

#### [GenAI](./GenAI/)
- **[bedrock_integration.py](./GenAI/bedrock_integration.py)** - Amazon Bedrock integration
- **[langchain_bedrock_integration.py](./GenAI/langchain_bedrock_integration.py)** - LangChain with Bedrock
- **[langchain_agent_bedrock.py](./GenAI/langchain_agent_bedrock.py)** - LangChain Agent with tools
- **[Vector Database](./GenAI/vector_db.md)** - Vector storage and retrieval
- **[S3 Vectors Tutorial](./GenAI/s3-vectors-tutorial.md)** - Complete S3 Vectors guide
- **[Prompt Engineering](./GenAI/bedrock_prompt_engineering.md)** - Best practices guide
- S3 vector operations and querying

### 🔐 Security & Identity

#### [IAM (Identity and Access Management)](./iam/)
- STS (Security Token Service) demonstrations
- MFA credentials setup
- Environment variables configuration

### 🚀 DevOps & CI/CD

#### [Development Tools](./dev-tools/)
- **[ci-cd](./dev-tools/ci-cd/)** - Complete CI/CD pipeline setup
- **[codebuild-reporting-junit-react](./dev-tools/codebuild-reporting-junit-react/)** - React app testing
- **[codepipeline-lambda-tester-function](./dev-tools/codepipeline-lambda-tester-function/)** - Pipeline testing
- **[cloudformation-deploy-shell](./dev-tools/cloudformation-deploy-shell/)** - Deployment automation
- **[c9-update-volume-size](./dev-tools/c9-update-volume-size/)** - Cloud9 storage management

### 🐳 Container Services

#### [Kubernetes/EKS](./kubernetes/)
- **[eks-helm-nodejs-app](./kubernetes/eks-helm-nodejs-app/)** - Helm chart for Node.js applications
- **[eks-simple-nginx](./kubernetes/eks-simple-nginx/)** - Basic Nginx deployment
- **[eks-simple-nodejs-app](./kubernetes/eks-simple-nodejs-app/)** - Simple Node.js application
- **[eks-prerequisites](./kubernetes/eks-prerequisites/)** - Installation scripts
- **[eks-pod-identity-test](./kubernetes/eks-pod-identity-test/)** - Pod identity configuration
- Traffic generation and monitoring samples

### 🛠️ SDK Examples

#### [AWS SDK](./sdk/)
- **[aws-secrets-manager-python-sdk](./sdk/aws-secrets-manager-python-sdk/)** - Secrets management
- **[get-ebs-snapshot-list-python](./sdk/get-ebs-snapshot-list-python/)** - EBS snapshot operations
- **[s3](./sdk/s3/)** - Comprehensive S3 operations
- **[ses](./sdk/ses/)** - Email service integration

### 📧 Sample Applications

#### [CloudAir Source](./cloudair-source/)
- **[TravelBuddy_DotNet](./cloudair-source/TravelBuddy_DotNet/)** - .NET travel application
- **[TravelBuddy_Java](./cloudair-source/TravelBuddy_Java/)** - Java travel application
- **[cloudair](./cloudair-source/cloudair/)** - Complete travel booking system

#### [Unicorn Web Project](./unicorn-web-project/)
- Sample web application with CI/CD integration

## 🚀 Getting Started

### Prerequisites
- AWS CLI configured
- Node.js (for CDK projects)
- Python 3.x (for Python examples)
- Docker (for containerized applications)
- kubectl and eksctl (for Kubernetes examples)

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd aws-samples

# Install dependencies for specific projects
cd cdk/demo-app && npm install
cd sam/apigtw-lambda-dynamodb-crud && sam build
```

## 📚 Key Technologies Covered

- **Infrastructure as Code**: CDK, CloudFormation, SAM
- **Serverless Computing**: Lambda, API Gateway, DynamoDB
- **Container Orchestration**: EKS, Kubernetes, Helm
- **Storage Solutions**: S3, EBS, EFS
- **AI/ML Services**: Bedrock, Rekognition, LangChain
- **Security**: IAM, STS, Secrets Manager
- **DevOps**: CodePipeline, CodeBuild, CodeDeploy
- **Monitoring**: CloudWatch, X-Ray

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.