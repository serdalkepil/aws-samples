#!/usr/bin/env python3
import boto3
AWS_REGION = "eu-central-1"
resource = boto3.resource("s3", region_name=AWS_REGION)
iterator = resource.buckets.all()
print("Listing Amazon S3 Buckets:")
for bucket in iterator:
    print(f"-- {bucket.name}")