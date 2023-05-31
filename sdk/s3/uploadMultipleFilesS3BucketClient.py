#!/usr/bin/env python3
import os
import pathlib
from glob import glob
import boto3
BASE_DIR = pathlib.Path(__file__).parent.resolve()
AWS_REGION = "us-east-2"
S3_BUCKET_NAME = "hands-on-cloud-demo-bucket"
S3_CLIENT = boto3.client("s3", region_name=AWS_REGION)
def upload_file(file_name, bucket, object_name=None, args=None):
    if object_name is None:
        object_name = file_name
    S3_CLIENT.upload_file(file_name, bucket, object_name, ExtraArgs=args)
    print(f"'{file_name}' has been uploaded to '{S3_BUCKET_NAME}'")

files = glob(f"{BASE_DIR}/files/*.txt")
for file in files:
    upload_file(file, S3_BUCKET_NAME)