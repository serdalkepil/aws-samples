import io
import boto3
AWS_REGION = "eu-central-1"
S3_BUCKET_NAME = "demo-bucket"
s3_client = boto3.client("s3", region_name=AWS_REGION)
def upload_generated_file_object(bucket, object_name):
    with io.BytesIO() as f:
        f.write(b'First line.\n')
        f.write(b'Second line.\n')
        f.seek(0)
        s3_client.upload_fileobj(f, bucket, object_name)
        print(f"Generated has been uploaded to '{bucket}'")
upload_generated_file_object(S3_BUCKET_NAME, 'generated_file.txt')