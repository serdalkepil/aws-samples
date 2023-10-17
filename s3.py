# get an object from S3

import boto3

s3 = boto3.client('s3')

response = s3.get_object(Bucket='my-bucket', Key='my-key')

print(response)


# create a new bucket with the name sk-34543534

import boto3

s3 = boto3.client('s3')

response = s3.create_bucket(Bucket='sk-34543534')

print(response)

