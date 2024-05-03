# from ast import Dict
# import boto3
# import os
# import pprint
# from tzlocal import get_localzone
# import pandas as pd

# def tzlocal():
#     tz = get_localzone();
#     return tz;
# aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
# aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
# aws_account_id = os.environ.get('AWS_ACCOUNT_ID')
# aws_account_name = os.environ.get('ACCOUNT_NAME')
# if aws_access_key_id is None or aws_secret_access_key is None:
#     print("Error: AWS credentials not set.")

# AccountDetails={
#         aws_account_id:{"Account":aws_account_name,"aws_access_key_id":aws_access_key_id,"aws_secret_access_key": aws_secret_access_key }
#         }


import boto3
import os
from tzlocal import get_localzone

def tzlocal():
    tz = get_localzone()
    return tz

# Read credentials from text file
credentials_file = r'C:\outputs\account_details.txt'
with open(credentials_file, 'r') as f:
    lines = f.readlines()

AccountDetails = {} 
# Loop through each line (each line contains credentials for one account)
for line in lines:
    account_details = line.strip().split(',')
    
    # Extract account details
    aws_account_id = account_details[0]
    aws_account_name = account_details[1]
    aws_access_key_id = account_details[2]
    aws_secret_access_key = account_details[3]
    
    # Check if credentials are set
    if aws_access_key_id is None or aws_secret_access_key is None:
        print(f"Error: AWS credentials not set for account {aws_account_id}")
        continue

    # Use credentials
    AccountDetails[aws_account_id] = {
            "Account": aws_account_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key
        }
    

    # Perform actions using boto3 or other AWS SDKs
    # Example:
    # client = boto3.client('sts', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # response = client.get_caller_identity()
    # print(response)