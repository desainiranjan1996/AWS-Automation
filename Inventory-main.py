#Author: Niranjan Desai
#CreatedDate: 28/04/2024
#Purpose: Pull EC2 inventory with all tags.
#ModifiedDate: 01/05/2024
#Modification: 1) Added function which sort the csv file columns in alphbetical order(line74).  
#------------  2) Column functionality which will check accounts in loop and add new columns 
#--------------  to CSV if that column is not present in previous account.

import boto3
import pandas as pd
import Credentials as cd
import os.path

# List to store instances from all regions
all_instances = []
#added 20/04/2024
filename = 'aws_instance_inventory_combined.csv'
file_exists = os.path.isfile(filename)

# Function to flatten tags
def flatten_tags(tags):
    flattened_tags = {}
    for tag in tags:
        flattened_tags[tag['Key']] = tag['Value']
    return flattened_tags

for account_id, credentials in cd.AccountDetails.items():
    # Extract credentials
    aws_access_key_id = credentials['aws_access_key_id']
    aws_secret_access_key = credentials['aws_secret_access_key']

    # AWS regions
    regions = ['ap-south-1']

    for regionName in regions:
        # Connect to EC2 for the current region
        ec2_client = boto3.client('ec2',
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  region_name=regionName)

        # Get instances
        response = ec2_client.describe_instances()

        instances = []

        # Extract instance information
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                internal_ip = instance.get('PrivateIpAddress', 'N/A')
                instance_status = instance['State']['Name']
                instance_name = ''
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        instance_name = tag['Value']
                        break
                instance_details = {
                    'AccountName': credentials['Account'],
                    'AccountId': account_id,
                    'InstanceName': instance_name,  # Modify this to get the instance name if available
                    'InstanceId': instance['InstanceId'],
                    'Region': regionName,
                    'InternalIpAddress': internal_ip,
                    'PublicIP': instance.get('PublicIpAddress','N/A'),
                    'InstanceStatus': instance_status,
                    **flatten_tags(instance.get('Tags', []))  # Flatten tags and unpack as separate columns
                }
                instances.append(instance_details)

        # Add instances from the current region to the list
        all_instances.extend(instances)

# Convert to DataFrame
df = pd.DataFrame(all_instances)

# Reorder columns alphabetically
df = df.reindex(sorted(df.columns), axis=1)

# Store as CSV
if file_exists and os.stat(filename).st_size != 0:
    # If the file exists and contains data, check for new columns
    existing_columns = pd.read_csv(filename, nrows=0).columns.tolist()
    new_columns = [col for col in df.columns if col not in existing_columns]

    # Append new columns to the existing CSV file
    if new_columns:
        df[new_columns].to_csv(filename, mode='a', header=False, index=False)
    
    # Append new data to the existing CSV file
    df.to_csv(filename, mode='a', header=False, index=False)
else:
    # If the file doesn't exist or is empty, write new data with column names
    df.to_csv(filename, index=False)
