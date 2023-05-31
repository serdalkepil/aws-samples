#!/usr/bin/env python3
import boto3
AWS_REGION = "eu-central-1"
resource = boto3.resource("s3", region_name=AWS_REGION)

bucket_name = "demo-bucket"
location = {'LocationConstraint': AWS_REGION}
bucket = resource.create_bucket(
    Bucket=bucket_name,
    CreateBucketConfiguration=location)
print("Amazon S3 bucket has been created")