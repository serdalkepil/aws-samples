#!/usr/bin/env python3
import boto3 
import json 
client = boto3.client('secretsmanager')
response = client.put_secret_value(
    SecretId='/prod/salesforceapikey',
    SecretString='{"username": "admin", "password": "my-secret-pwd-new"}'
)
print(response)