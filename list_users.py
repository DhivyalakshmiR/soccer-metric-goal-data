import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

def list_users():
    iam = boto3.client(
        "iam",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    paginator = iam.get_paginator('list_users')
    for response in paginator.paginate():
        for user in response["Users"]:
            print(f"Username: {user['UserName']}, Arn: {user['Arn']}")

list_users()
