#Author: Niranjan Desai
#Date: 30/04/2024
#Purpose: This script will replace all the incorrect combination of 'CXIO managed' tag with new "CXIO_MS" tag.


import boto3
import csv
import re
import Credentials as cd

# Specify the hardcoded region
region = 'ap-south-1'  # Replace with your desired region

# Iterate over account details from Credentials module
for accList in cd.AccountDetails:
    accId = 0
    accId = accList.strip()
    accCred = dict(cd.AccountDetails[accId])
    accountName = accCred['Account'].strip()
    aws_access_key_id = accCred['aws_access_key_id']
    aws_secret_access_key = accCred['aws_secret_access_key']
    
    # Initialize EC2 client
    ec2_client = boto3.client('ec2',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=region)

    # Read data from CSV and add/remove tags
    with open('instances_need_to_be_tagged.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            account_number = row['AccountNumber']
            instance_id = row['InstanceID']
            tag_value = row['CXIO_MS']
            
            # Check if the row belongs to the current account
            if account_number.strip() == accId:
                try:
                    # Set tags for the EC2 instance
                    response = ec2_client.create_tags(
                        Resources=[instance_id],
                        Tags=[{'Key': 'CXIO_MS', 'Value': tag_value}]
                    )
                    print(f"Tag '{tag_value}' set successfully for instance {instance_id} in account {accountName}.")

                    # Define regex pattern for tag keys to remove
                    tag_key_pattern = re.compile(r'^(cxio[_ -]managed)$', re.IGNORECASE)
                    
                    # Describe tags for the EC2 instance
                    response = ec2_client.describe_tags(
                        Filters=[
                            {'Name': 'resource-id', 'Values': [instance_id]}
                        ]
                    )
                    
                    # Extract tag keys from the response and remove tags with matched keys
                    tags = response.get('Tags', [])
                    keys_to_remove = [tag['Key'] for tag in tags if tag_key_pattern.match(tag['Key'])]
                    
                    # Remove tags with matched keys for the EC2 instance
                    if keys_to_remove:
                        response = ec2_client.delete_tags(
                            Resources=[instance_id],
                            Tags=[{'Key': key} for key in keys_to_remove]
                        )
                        print(f"Tags removed successfully for instance {instance_id} in account {accountName}.")
                    else:
                        print(f"No matching tags found for instance {instance_id} in account {accountName}.")
                except Exception as e:
                    print(f"Error occurred for instance {instance_id}: {str(e)}")
