#!/usr/bin/env python3
import pathlib
import boto3

BASE_DIR = pathlib.Path(__file__).parent.resolve()
AWS_REGION = "eu-central-1"
S3_BUCKET_NAME = "demo-bucket"
s3_client = boto3.client("s3", region_name=AWS_REGION)

def upload_file(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name
    s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    print(f"'{file_name}' has been uploaded to '{S3_BUCKET_NAME}'")

upload_file(f"{BASE_DIR}/files/demo.txt", S3_BUCKET_NAME)