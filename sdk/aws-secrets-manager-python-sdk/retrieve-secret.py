#!/usr/bin/env python3
import boto3 
import json 
client = boto3.client('secretsmanager')
response = client.get_secret_value(
    SecretId='/$stage/salesforceapikey'
)
database_secrets = json.loads(response['SecretString'])
print(database_secrets['username'])
print(database_secrets['password'])
