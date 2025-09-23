# EC2 Instance Demo with On-Demand and Spot Instances - Amazon Linux 2023

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Guide](#step-by-step-guide)
4. [On-Demand Instance Creation](#on-demand-instance-creation)
5. [Spot Instance Creation](#spot-instance-creation)
6. [Verification](#verification)
7. [Cost Comparison](#cost-comparison)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Overview

This guide demonstrates how to create both On-Demand and Spot EC2 instances using Amazon Linux 2023 AMI with custom user data for automated web server setup.

## Prerequisites

- AWS Account with appropriate permissions
- Basic understanding of EC2 instances
- Key Pair for SSH access (optional for this demo)

## Step-by-Step Guide

### On-Demand Instance Creation

#### Step 1: Navigate to EC2 Dashboard

1. Login to AWS Management Console
2. Search for "EC2" in services or navigate to EC2 Dashboard
3. Click "Launch Instance"

#### Step 2: Configure Instance Details

**Basic Configuration:**

- **Name**: `ondemand-al2023-web-server`
- **AMI**: Amazon Linux 2023 AMI (Search for "Amazon Linux 2023" in AMI catalog)
- **Instance Type**: t3.micro (free tier eligible)
- **Key Pair**: Select existing or create new key pair (optional for web access)

**Network Settings:**

- **VPC**: Default VPC
- **Subnet**: Any availability zone
- **Auto-assign Public IP**: Enable
- **Security Groups**: Create new security group

#### Step 3: Configure Security Group

Create security group `web-sg-al2023` with rules:

- **Type**: HTTP, Port: 80, Source: 0.0.0.0/0
- **Type**: SSH, Port: 22, Source: My IP (optional for management)

#### Step 4: Advanced Details - User Data

Scroll down to **Advanced Details** section and paste the following user data script:

```bash
#!/bin/bash
# Update system and install Apache (httpd)
dnf update -y
dnf install -y httpd wget
systemctl enable httpd
systemctl start httpd

# Get instance metadata
AMI_ID=$(curl -s http://169.254.169.254/latest/meta-data/ami-id)
PUBLIC_HOSTNAME=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
INSTANCE_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

# Create custom HTML page
cat > /var/www/html/index.html << EOF
<html>
<head>
    <title>Amazon Linux 2023 Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #232f3e; color: white; padding: 20px; border-radius: 5px; }
        .info { background: #f1f1f1; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .spot-badge { background: #ff9900; color: white; padding: 5px 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Amazon Linux 2023 Web Server</h1>
            <h2>On-Demand Instance Demo</h2>
        </div>
        
        <div class="info">
            <h3>Instance Metadata:</h3>
            <p><strong>AMI ID:</strong> $AMI_ID</p>
            <p><strong>Public Hostname:</strong> $PUBLIC_HOSTNAME</p>
            <p><strong>Instance Type:</strong> $INSTANCE_TYPE</p>
            <p><strong>Availability Zone:</strong> $AZ</p>
            <p><strong>Instance Lifecycle:</strong> On-Demand</p>
        </div>
        
        <div>
            <h3>Server Information:</h3>
            <p><strong>OS:</strong> Amazon Linux 2023</p>
            <p><strong>Web Server:</strong> Apache HTTPD</p>
            <p><strong>Status:</strong> <span style="color: green;">● Running</span></p>
        </div>
    </div>
</body>
</html>
EOF

# Set proper permissions
chown apache:apache /var/www/html/index.html
systemctl restart httpd

# Create a health check file
echo "Healthy" > /var/www/html/health.html

# Print completion message
echo "User data script completed successfully at $(date)" >> /var/log/user-data.log
```

### Spot Instance Creation

#### Step 1: Launch New Instance

Return to EC2 Dashboard

Click "Launch Instance"

#### Step 2: Configure Spot Instance Details

**Basic Configuration:**

- **Name**: `spot-al2023-web-server`
- **AMI**: Amazon Linux 2023 AMI (Search for "Amazon Linux 2023" in AMI catalog)
- **Instance Type**: t3.micro (free tier eligible)
- **Key Pair**: Select existing or create new key pair (optional for web access)

**Network Settings:**

- **VPC**: Default VPC
- **Subnet**: Any availability zone
- **Auto-assign Public IP**: Enable
- **Security Groups**: Create new security group

**Purchase Option:**

- **Purchase option:** ✅ Check "Request Spot Instances"

**Spot Request Settings:**

- **Request type:** Persistent (recommended for demo)
- **Interruption behavior:** Stop (preserves root volume)
- **Maximum price:** Leave as "On-Demand price" (recommended)

#### Step 3: Configure Spot Instance Security Group

Use existing security group: web-sg-al2023

#### Step 4: Advanced Details Spot Instance - User Data 

Use modified user data script for Spot instance:

```bash
#!/bin/bash
# Update system and install Apache (httpd)
dnf update -y
dnf install -y httpd wget
systemctl enable httpd
systemctl start httpd

# Get instance metadata
AMI_ID=$(curl -s http://169.254.169.254/latest/meta-data/ami-id)
PUBLIC_HOSTNAME=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
INSTANCE_TYPE=$(curl -s http://169.254.169.254/latest/meta-data/instance-type)
AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)

# Create custom HTML page for Spot instance
cat > /var/www/html/index.html << EOF
<html>
<head>
    <title>Amazon Linux 2023 Spot Instance</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #232f3e; color: white; padding: 20px; border-radius: 5px; }
        .info { background: #f1f1f1; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .spot-badge { background: #ff9900; color: white; padding: 5px 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Amazon Linux 2023 Web Server</h1>
            <h2><span class="spot-badge">SPOT INSTANCE</span> Demo</h2>
        </div>
        
        <div class="info">
            <h3>Instance Metadata:</h3>
            <p><strong>AMI ID:</strong> $AMI_ID</p>
            <p><strong>Public Hostname:</strong> $PUBLIC_HOSTNAME</p>
            <p><strong>Instance Type:</strong> $INSTANCE_TYPE</p>
            <p><strong>Availability Zone:</strong> $AZ</p>
            <p><strong>Instance Lifecycle:</strong> <span class="spot-badge">Spot Instance</span></p>
            <p><strong>Cost Savings:</strong> Up to 90% compared to On-Demand</p>
        </div>
        
        <div class="warning">
            <h3>⚠️ Spot Instance Notice:</h3>
            <p>This instance may be interrupted with a 2-minute warning if Spot capacity is needed.</p>
            <p>Data persistence is maintained through EBS volumes.</p>
        </div>
        
        <div>
            <h3>Server Information:</h3>
            <p><strong>OS:</strong> Amazon Linux 2023</p>
            <p><strong>Web Server:</strong> Apache HTTPD</p>
            <p><strong>Status:</strong> <span style="color: green;">● Running</span></p>
        </div>
    </div>
</body>
</html>
EOF

# Set proper permissions
chown apache:apache /var/www/html/index.html
systemctl restart httpd

# Create interruption notice handler script
cat > /usr/local/bin/spot-interruption-handler.sh << 'EOF'
#!/bin/bash
# Spot Instance Interruption Handler
echo "Spot interruption notice received at $(date)" >> /var/log/spot-interruption.log
# Add any cleanup tasks here before instance termination
EOF

chmod +x /usr/local/bin/spot-interruption-handler.sh

# Print completion message
echo "Spot instance user data script completed at $(date)" >> /var/log/user-data.log
```

#### Step 5: Launch Spot Instance

Click "Launch Instance"

The spot request will be created and fulfilled when capacity is available

### Verification

- Check Instance Status
- Go to EC2 Dashboard → Instances
- Verify both instances are running - Note the public IP addresses

### Test Web Servers

Open web browser and navigate to:

- On-Demand: `http://<ON-DEMAND-PUBLIC-IP>`
- Spot: `http://<SPOT-PUBLIC-IP>`

You should see the custom HTML pages with instance metadata

### Verify User Data Execution

Connect via SSH or SSM Session Manager:

```bash
ssh -i your-key.pem ec2-user@<instance-ip>
```

Check user data logs:

```bash
tail -f /var/log/user-data.log
```

Check Apache status:

```bash
sudo systemctl status httpd
```

### Cost Comparison

#### On-Demand Pricing (t3.micro)

us-east-1: ~$0.0104 per hour

Monthly (730 hours): ~$7.59

#### Spot Pricing (t3.micro)

us-east-1: ~$0.0031 per hour (70% savings)

Monthly (730 hours): ~$2.26

#### Estimated Savings

Hourly Savings: 70%

Monthly Savings: ~$5.33 per instance

### Best Practices

#### For On-Demand Instances

- Use for critical, always-on workloads
- Ideal for production environments
- Predictable billing

#### For Spot Instances

- Use for fault-tolerant workloads
- Implement checkpointing for long-running jobs
- Use across multiple availability zones
- Combine with Auto Scaling groups
- Monitor spot instance interruptions

### User Data Best Practices

- Always start with #!/bin/bash
- Use -y flag for unattended installations
- Implement proper error handling
- Log script execution for debugging
- Use instance metadata for dynamic configuration

#### Troubleshooting

User data not executing

- Check cloud-init logs: /var/log/cloud-init-output.log
- Verify script syntax
- - Check if #! shebang is present
- Spot instance not fulfilled:
- - Try different instance types
- - Check spot price history
- - Modify maximum price
- Web server not accessible:
- - Verify security group allows HTTP (port 80)
- - Check if Apache is running: sudo systemctl status httpd
- - Examine Apache logs: /var/log/httpd/error_log

#### Useful Commands for Debugging:

```bash
# Check user data execution logs
sudo cat /var/log/cloud-init-output.log

# Check cloud-init status
sudo cloud-init status

# Verify Apache installation
sudo systemctl status httpd

# Check listening ports
sudo netstat -tlnp

# Test local web server
curl http://localhost
```

### Monitoring Spot Instances

#### Spot Request Status

EC2 Dashboard → Spot Requests

Monitor status: fulfilled, pending-fulfillment, or cancelled

Instance Interruption Notices:

Use Instance Metadata Service:

```bash
curl http://169.254.169.254/latest/meta-data/spot/instance-action
```

#### CloudWatch Metrics

- Monitor Spot interruption rates
- Set up alarms for instance status checks

This demo provides a complete hands-on experience with both On-Demand and Spot instances using Amazon Linux 2023, highlighting the cost benefits and use cases for each pricing model.