import boto3
import json
from datetime import datetime
import os

def fetch_aws_permissions():
    iam = boto3.client('iam')
    
    policies = []
    paginator = iam.get_paginator('list_policies')
    for page in paginator.paginate(Scope='AWS'):
        policies.extend(page['Policies'])
    
    detailed_policies = []
    for policy in policies:
        policy_version = iam.get_policy_version(
            PolicyArn=policy['Arn'],
            VersionId=policy['DefaultVersionId']
        )
        detailed_policies.append({
            'PolicyName': policy['PolicyName'],
            'PolicyDocument': policy_version['PolicyVersion']['Document']
        })
    
    os.makedirs('snapshots/aws', exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'snapshots/aws/aws_permissions_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(detailed_policies, f, indent=2)
    with open('snapshots/aws/aws_permissions_latest.json', 'w') as f:
        json.dump(detailed_policies, f, indent=2)
    with open('snapshots/aws/aws_last_snapshot.txt', 'w') as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    fetch_aws_permissions()