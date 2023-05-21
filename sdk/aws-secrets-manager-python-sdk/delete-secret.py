#!/usr/bin/env python3
import boto3
client = boto3.client('secretsmanager')
response = client.delete_secret(
    SecretId='DatabaseProdSecrets',
    RecoveryWindowInDays=7,
    ForceDeleteWithoutRecovery=False
)
print(response)