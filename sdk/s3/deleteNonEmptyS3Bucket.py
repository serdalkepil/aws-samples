#!/usr/bin/env python3
import io
import boto3
AWS_REGION = "eu-central-1"
S3_BUCKET_NAME = "demo-bucket"

s3_resource = boto3.resource("s3", region_name=AWS_REGION)
s3_bucket = s3_resource.Bucket(S3_BUCKET_NAME)

def cleanup_s3_bucket():
    # Deleting objects
    for s3_object in s3_bucket.objects.all():
        s3_object.delete()
    # Deleting objects versions if S3 versioning enabled
    for s3_object_ver in s3_bucket.object_versions.all():
        s3_object_ver.delete()
    print("S3 Bucket cleaned up")

cleanup_s3_bucket()
s3_bucket.delete()
print("S3 Bucket deleted")