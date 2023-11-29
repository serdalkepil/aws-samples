# generate a method to create a bucket 

import boto3

def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    s3.create_bucket(Bucket=bucket_name)
    print(f"Bucket {bucket_name} created successfully!")
    
# Example usage

create_bucket('XXXXXXXXX')

# This will create a bucket named XXXXXXXXX in your default region.

# You can also specify a region like this:

# create_bucket('XXXXXXXXX', 'XXXXXXXXX')

# generate a method to list all buckets

import boto3

def list_buckets():
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

        

