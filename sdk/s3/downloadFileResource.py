#!/usr/bin/env python3
import io
import boto3
AWS_REGION = "us-east-2"
S3_BUCKET_NAME = "hands-on-cloud-demo-bucket"
s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_object = s3_resource.Object(S3_BUCKET_NAME, 'demo.txt')
s3_object.download_file('/tmp/demo.txt')
print('S3 object download complete')