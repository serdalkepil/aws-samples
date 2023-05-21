import boto3
client = boto3.client('secretsmanager')
response = client.list_secrets()
print(response['SecretList'])