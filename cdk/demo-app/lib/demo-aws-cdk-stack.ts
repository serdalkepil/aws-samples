import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import { Construct } from 'constructs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export class DemoAwsCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Create S3 Bucket for Image Storage
    const imageBucket = new s3.Bucket(this, 'ImageStorageBucket', {
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true
    });

    // Create DynamoDB Table for Metadata
    const imageMetadataTable = new dynamodb.Table(this, 'ImageMetadataTable', {
      partitionKey: { name: 'imageId', type: dynamodb.AttributeType.STRING },
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });

    // Lambda Function for Image Processing
    const imageProcessorLambda = new lambda.Function(this, 'ImageProcessorLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(join(__dirname, '../lambda')),
      environment: {
        DYNAMODB_TABLE: imageMetadataTable.tableName,
        S3_BUCKET: imageBucket.bucketName
      }
    });

    // Grant Lambda permissions to interact with DynamoDB and S3
    imageMetadataTable.grantReadWriteData(imageProcessorLambda);
    imageBucket.grantRead(imageProcessorLambda);

    // Configure S3 bucket to trigger Lambda on new object
    imageBucket.addEventNotification(
      s3.EventType.OBJECT_CREATED,
      new s3n.LambdaDestination(imageProcessorLambda)
    );

    // Create VPC for EC2 Instance
    const vpc = new ec2.Vpc(this, 'DemoVPC', {
      maxAzs: 2,
      natGateways: 1
    });

    // Security Group for EC2
    const securityGroup = new ec2.SecurityGroup(this, 'EC2SecurityGroup', {
      vpc,
      allowAllOutbound: true,
      description: 'Security group for demo EC2 instance'
    });

    // Add inbound SSH rule
    securityGroup.addIngressRule(
      ec2.Peer.anyIpv4(),
      ec2.Port.tcp(22),
      'Allow SSH access from anywhere'
    );

    // EC2 Instance
    const ec2Instance = new ec2.Instance(this, 'DemoEC2Instance', {
      vpc,
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.latestAmazonLinux2023(),
      securityGroup: securityGroup
    });

    // Outputs
    new cdk.CfnOutput(this, 'BucketName', { 
      value: imageBucket.bucketName,
      description: 'S3 Bucket for Image Storage'
    });

    new cdk.CfnOutput(this, 'DynamoDBTableName', { 
      value: imageMetadataTable.tableName,
      description: 'DynamoDB Table for Image Metadata'
    });

    new cdk.CfnOutput(this, 'LambdaFunctionName', { 
      value: imageProcessorLambda.functionName,
      description: 'Lambda Function for Image Processing'
    });

    new cdk.CfnOutput(this, 'EC2InstanceId', { 
      value: ec2Instance.instanceId,
      description: 'EC2 Instance ID'
    });

    new cdk.CfnOutput(this, 'EC2InstancePublicIP', { 
      value: ec2Instance.instancePublicIp,
      description: 'Public IP of the EC2 Instance'
    });
  }
}