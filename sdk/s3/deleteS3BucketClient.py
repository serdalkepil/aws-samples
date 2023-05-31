#!/usr/bin/env python3
import boto3
AWS_REGION = "eu-central-1"
client = boto3.client("s3", region_name=AWS_REGION)
bucket_name = "demo-bucket"
client.delete_bucket(Bucket=bucket_name)
print("Amazon S3 Bucket has been deleted")