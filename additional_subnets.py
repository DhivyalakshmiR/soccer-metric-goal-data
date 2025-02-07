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

subnets_to_create = [
    {"CidrBlock": "192.168.2.0/24", "AvailabilityZone": "ap-south-1b"},
    {"CidrBlock": "192.168.3.0/24", "AvailabilityZone": "ap-south-1c"}
]

subnet_ids = []
for subnet in subnets_to_create:
    response = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=subnet["CidrBlock"],
        AvailabilityZone=subnet["AvailabilityZone"]
    )
    subnet_id = response["Subnet"]["SubnetId"]
    subnet_ids.append(subnet_id)
    print(f"Created subnet {subnet_id} in {subnet['AvailabilityZone']} with CIDR {subnet['CidrBlock']}")

print("All subnet IDs:", subnet_ids)
