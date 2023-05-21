#!/usr/bin/env python3
import boto3
client = boto3.client('secretsmanager')
response = client.create_secret(
    Name='/prod/salesforceapikey',
    SecretString='{"username": "admin", "password": "my-secret-pwd"}'
)
print(response)