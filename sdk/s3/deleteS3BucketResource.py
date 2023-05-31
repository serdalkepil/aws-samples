#!/usr/bin/env python3
import boto3
AWS_REGION = "eu-central-1"
resource = boto3.resource("s3", region_name=AWS_REGION)
bucket_name = "demo-bucket"
s3_bucket = resource.Bucket(bucket_name)
s3_bucket.delete()
print("Amazon S3 Bucket has been deleted")