import boto3
import os
        
def lambda_handler(event, context):
    print('event: ', event)
    print('context: ', context)
    print('environment: ',os.environ)
    
    bucketName = event['bucket_name']
    key = event['object_key']
    s3 = boto3.client('s3', region_name=os.environ['AWS_REGION'])
    sqlExpression = f"Select * from s3object s where s.country='{event['country']}'"
    
    print('sqlExpression: ', sqlExpression)
    
    try:
        response = s3.select_object_content(
            Bucket = bucketName,
            Key = key,
            ExpressionType = 'SQL',
            Expression = sqlExpression,
            InputSerialization = {'CSV': {"FileHeaderInfo": "Use"}},
            OutputSerialization = {'JSON': {}},
        )
    except botocore.exceptions.ClientError as e:
        print("Unexpected error: %s" % e)
    
    for event in response['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
            
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Bytes scanned: ")
            print(statsDetails['BytesScanned'])
            print("Bytes processed: ")
            print(statsDetails['BytesProcessed'])
            
