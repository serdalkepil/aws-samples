#!/usr/bin/env python3
import boto3
AWS_REGION = "eu-central-1"
client = boto3.client("s3", region_name=AWS_REGION)
response = client.list_buckets()
print("Listing Amazon S3 Buckets:")

for bucket in response['Buckets']:
    print(f"-- {bucket['Name']}")