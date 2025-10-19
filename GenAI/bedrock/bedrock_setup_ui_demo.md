# AWS Bedrock Demo Setup & Testing Guide

## Demo Setup

### 1. Create IAM User and Configure Permissions

#### Create IAM User
1. Log into AWS Console
2. Navigate to **IAM** → **Users** → **Create user**
3. User name: `bedrock-demo-user`
4. Select **Access key - Programmatic access**
5. Click **Next**

#### Attach Permissions
1. Select **Attach policies directly**
2. Search for and select: **AmazonBedrockFullAccess**
3. Click **Next** → **Create user**
4. **Important**: Download or copy the Access Key ID and Secret Access Key

### 2. Install AWS CLI

#### Windows
```bash
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi
```

#### macOS
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

#### Linux
```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

#### Verify Installation
```bash
aws --version
```

### 3. Configure AWS CLI

Run the configuration command:
```bash
aws configure
```

Enter the following when prompted:
- **AWS Access Key ID**: [Your Access Key]
- **AWS Secret Access Key**: [Your Secret Key]
- **Default region name**: `us-east-1` (or your preferred region)
- **Default output format**: `json`

### 4. Verify Configuration

#### Check Identity
```bash
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/bedrock-demo-user"
}
```

#### List Inference Profiles
```bash
aws bedrock list-inference-profiles
```

#### List Foundation Models
```bash
aws bedrock list-foundation-models
```

---

## Module 3: Bedrock UI Testing Scenarios

### Scenario 1: Basic Pizza Restaurant Query

**Prompt:**
```
Recommend the top 5 pizza restaurants in Seattle, Washington
```

**Expected Behavior**: The model should provide a list of popular pizza restaurants in Seattle.

---

### Scenario 2: Follow-up Location Query

**Prompt:**
```
Which one is closest to downtown?
```

**Expected Behavior**: The model should reference the previous list and identify which restaurant is nearest to downtown Seattle (tests conversation memory).

---

### Scenario 3: Formatted Response

**Prompt:**
```
Recommend top 5 pizza restaurants in Seattle, Washington

Response should follow the below format:
- Rank number, restaurant name, stars
- Number of positive reviews considered
- Brief restaurant description (25 words or less)
```

**Expected Output Format:**
```
1. [Restaurant Name], ⭐⭐⭐⭐⭐
   - [X] positive reviews
   - [Brief 25-word description]

2. [Restaurant Name], ⭐⭐⭐⭐
   - [X] positive reviews
   - [Brief 25-word description]

...
```

---

### Scenario 4: Web-Based Research Query

**Prompt:**
```
Answer the below question based on the website: https://docs.aws.amazon.com/

What AWS services can be used for Compute?
Just list the service name in bullet-list format
```

**Expected Output Format:**
```
- Amazon EC2
- AWS Lambda
- Amazon ECS
- Amazon EKS
- AWS Batch
- AWS Elastic Beanstalk
- Amazon Lightsail
- AWS Fargate
- AWS Outposts
- AWS Wavelength
```

**Note**: This tests the model's ability to retrieve and process information from external sources (if the model has web access capabilities).

---

### Scenario 5: Image Generation

**Prompt:**
```
Image generation: skyline of New York City at night
```

**Expected Behavior**: 
- If using a model with image generation capabilities (e.g., Amazon Titan Image Generator, Stable Diffusion):
  - Should generate an image showing NYC skyline
  - Should include nighttime lighting (building lights, dark sky)
  - May include landmarks like Empire State Building, One World Trade Center
  
**Model Selection**: 
- Navigate to Bedrock Console → Image Generation
- Select: **Amazon Titan Image Generator G1** or **Stability AI Stable Diffusion XL**
- Enter the prompt
- Click **Generate**

---

## Testing Checklist

- [ ] IAM user created with BedrockFullAccess
- [ ] AWS CLI installed and version verified
- [ ] AWS CLI configured with access keys
- [ ] `aws sts get-caller-identity` successful
- [ ] `aws bedrock list-inference-profiles` returns results
- [ ] `aws bedrock list-foundation-models` returns results
- [ ] Bedrock Console accessible
- [ ] Scenario 1: Basic query tested
- [ ] Scenario 2: Follow-up query tested (conversation memory)
- [ ] Scenario 3: Formatted response tested
- [ ] Scenario 4: Web-based query tested
- [ ] Scenario 5: Image generation tested

---

## Important Notes

### Model Availability
- Not all models are available in all regions
- Some models require explicit access requests
- Check Bedrock Console → Model Access to enable models

### Pricing Considerations
- Text generation: Charged per 1000 input/output tokens
- Image generation: Charged per image
- Refer to AWS Bedrock pricing page for current rates

### Best Practices
1. Always test with small requests first
2. Enable CloudWatch logging for debugging
3. Use appropriate model for task (text vs. image)
4. Set guardrails for production use
5. Monitor costs in AWS Cost Explorer

---

## Troubleshooting

### "Access Denied" Errors
- Verify BedrockFullAccess policy is attached
- Check if model access is enabled in Bedrock Console
- Ensure correct region is configured

### CLI Commands Failing
- Verify AWS CLI is latest version
- Check credentials with `aws sts get-caller-identity`
- Ensure region supports Bedrock service

### Image Generation Not Working
- Verify you selected an image generation model
- Check model access in Bedrock Console
- Some models have content filtering that may block certain prompts