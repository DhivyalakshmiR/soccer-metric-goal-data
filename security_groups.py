import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region = os.getenv("AWS_DEFAULT_REGION")
vpc_id = os.getenv("VPC_ID") 

ec2 = boto3.client("ec2", aws_access_key_id=aws_access_key,
                   aws_secret_access_key=aws_secret_key,
                   region_name=region)

response = ec2.create_security_group(
    GroupName="MWAA-Security-Group",
    Description="Security group for MWAA environment",
    VpcId=vpc_id
)

mwaa_sg_id = response["GroupId"]
print(f"MWAA Security Group Created: {mwaa_sg_id}")

ec2.authorize_security_group_ingress(
    GroupId=mwaa_sg_id,
    IpPermissions=[
        {
            "IpProtocol": "tcp",
            "FromPort": 443,
            "ToPort": 443,
            "IpRanges": [{"CidrIp": "0.0.0.0/0"}]
        }
    ]
)

print("Inbound rules added successfully!")
