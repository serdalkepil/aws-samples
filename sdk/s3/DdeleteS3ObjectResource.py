#!/usr/bin/env python3
import boto3
AWS_REGION = "us-east-2"
S3_BUCKET_NAME = "demo-bucket"
s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_object = s3_resource.Object(S3_BUCKET_NAME, 'new_demo.txt')
    
s3_object.delete()
print('S3 object deleted')