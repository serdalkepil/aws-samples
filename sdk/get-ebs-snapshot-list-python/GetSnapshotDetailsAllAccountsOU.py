from multiprocessing import active_children
import boto3
import subprocess, csv, os, json
import argparse, logging

# Enable Logging
logging.basicConfig(filename='GetSnapshotDetailsAllAccountsOU_debug.log', level=logging.INFO)

# Define the Global variable here
subprocess.call (["clear"], shell = True)
field_names=['Account', 'Snapshot_Id', 'Volume_Size', 'Volume_Id', 'start_time', 'Owner','Team','instance_id','Description']
rows = []

# Function to get all accounts for your Org
def getallAccounts():
    print('Getting all AWS Accounts')
    # create empty list for all member Accounts
    accountList = []
    # create boto3 client
    client = boto3.client('organizations')
    paginator = client.get_paginator('list_accounts')
    try:
        # Get all AWS Accounts as reported by AWS Organizations from DDB
        iterator = paginator.paginate()
        for page in iterator:
            for Account in page['Accounts']:
                if Account['Status'] == 'ACTIVE':
                    accountList.append(Account['Id'])
                else:
                    logging.info('Account ' + Account['Id'] + ' is not Active, skipping!')
                    pass
    except Exception as e:
        raise e
    return accountList

# Function to assume role function for given account
def assume_role(target_account, role):
    '''
      Description: Get cross account credentials for given AWS target account
      Arguments:
          master_role_arn: Master account role ARN
          target_account: Target account number
      Returns: assubmed cross account role credentials
    '''
    sts = boto3.client('sts')
    try:
        assume_role_object = sts.assume_role(
            RoleArn="arn:aws:iam::" + target_account + ":role/"+ role,
            RoleSessionName='AssumingCrossAccountRole'
        )
    except Exception as err:
        logging.error("Error ocurred while assuming role: {}".format(err))
        return False
    
    role_dict = dict()
    role_dict['AccessKeyId'] = assume_role_object['Credentials']['AccessKeyId']
    role_dict['SecretAccessKey'] = assume_role_object['Credentials']['SecretAccessKey']
    role_dict['SessionToken'] = assume_role_object['Credentials']['SessionToken']
    return role_dict

# Function to get the list of snapshots for given account
def getallsnapshots(act, client):
    response = client.describe_snapshots(OwnerIds=[act], MaxResults=1000)
    snapshotList = response["Snapshots"]
    logging.info(f'Number of Snapshots {len(snapshotList)}')
    print(f'Number of Snapshots {len(snapshotList)}')
    i=0
    if len(snapshotList) != 0:
        for snap in snapshotList:
            if "Tags" in snap:
                tags = snap['Tags']
            else:
                tags = None
            build_rows_dictionary(act,snap['SnapshotId'],snap['VolumeSize'],snap['VolumeId'],snap['StartTime'],snap['Description'],tags)
        while('NextToken' in response):
            i=i+1
            if (i % 11 == 0): write_csv(file)
            response = client.describe_snapshots(OwnerIds=[act], MaxResults=2000, NextToken=response['NextToken'])
            snapshotList=response["Snapshots"]
            logging.info(f'Number of Snapshots {len(snapshotList)}')
            print(f'Number of Snapshots {len(snapshotList)}')
            if len(snapshotList) != 0:
                for snap in snapshotList:
                    if "Tags" in snap:
                        tags = snap['Tags']
                    else:
                        tags = None
                    build_rows_dictionary(act,snap['SnapshotId'],snap['VolumeSize'],snap['VolumeId'],snap['StartTime'],snap['Description'],tags)


# Function to build dictionary with required field on snapshots
def build_rows_dictionary(account, snapshot_id, volume_size, volume_id, start_time, description, tags):
    row_dict={}
    row_dict["Account"]=account
    row_dict["Snapshot_Id"]=snapshot_id
    row_dict["Volume_Size"]=volume_size
    row_dict["Volume_Id"]=volume_id
    row_dict["start_time"]=start_time
    row_dict["Description"]=description
    if tags:
        for x in tags:
            if x['Key'] == "Owner":
                row_dict["Owner"]=x['Value']
            elif x['Key'] == "Team":
                row_dict["Team"]=x['Value']
            elif x['Key'] == "instance_id":
                row_dict["instance_id"]=x['Value']
    rows.append(row_dict)
        
# Function to write dictionary to CSV
def write_csv (filepath):
    with open(filepath, 'w') as f:
        csv_writer = csv.DictWriter(f, field_names)
        csv_writer.writeheader()
        csv_writer.writerows(rows) 
        
def main():
    sts_client = boto3.client("sts")
    current_account = sts_client.get_caller_identity()["Account"]
    client = boto3.client('ec2', region_name=region)
    if (arole != None):
        accounts = getallAccounts()
        logging.info(f'Accounts found --> {len(accounts)}')
        for act in accounts:
            if act == current_account or act == None:
                logging.info("Account number "+ act)
            else:
                logging.info("Account number "+ act)
                credentials=assume_role(act, arole)
                try: 
                    client = boto3.client('ec2', 
                        region_name=region,
                        aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'])
                except:
                    logging.info("Can't assume the role in account "+ act)
            getallsnapshots(act, client)
    else:
        getallsnapshots(current_account, client)
    
    write_csv(file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates a CSV report about EBS volumes and tracks snapshots on them.')
    parser.add_argument('--region', required=True, help='AWS region such as us-east-1')
    parser.add_argument('--file', required=True, help='Path for output CSV file')
    parser.add_argument('--role', required=False, help='IAM role that script can assume in other accounts')
    try:
        args = parser.parse_args()
        file=args.file
        region=args.region
        arole=args.role
    except NameError:
        logging.error( "Required arguments are missing. Please provide path for the file and aws region")

    if os.path.exists(file):
        raise Exception("File already exists!")
    else:
        main()