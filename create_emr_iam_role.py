import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

iam = boto3.client(
    "iam",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

def create_emr_iam_role(role_name, service, policy_arn):
    """Creates an IAM role with an assume role policy for EMR."""
    assume_role_policy_document = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": service},
                "Action": "sts:AssumeRole"
            }
        ]
    })

    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy_document
        )
        print(f"✅ Created IAM Role: {role_name}")

        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        print(f"✅ Attached Policy: {policy_arn} to {role_name}")

        return response["Role"]["Arn"]

    except iam.exceptions.EntityAlreadyExistsException:
        print(f"⚠️ IAM Role {role_name} already exists.")
        return None

create_emr_iam_role(
    role_name="EMR_EC2_DefaultRole",
    service="ec2.amazonaws.com",
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
)

create_emr_iam_role(
    role_name="EMR_DefaultRole",
    service="elasticmapreduce.amazonaws.com",
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
)
