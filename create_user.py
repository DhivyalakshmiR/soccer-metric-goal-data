import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

def create_user(username):
    iam = boto3.client(
        "iam",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    response = iam.create_user(UserName=username)
    print(response)

create_user("project1_demo") 
