import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")
subnet_id = os.getenv("AWS_SUBNET_ID") 

emr_client = boto3.client(
    "emr",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

cluster_params = {
    "Name": "My-Spark-EMR-Cluster",
    "ReleaseLabel": "emr-6.12.0",  
    "Applications": [{"Name": "Spark"}], 
    "Instances": {
        "InstanceCount": 1,  
        "KeepJobFlowAliveWhenNoSteps": True,  
        "Ec2SubnetId": subnet_id,  
        "MasterInstanceType": "m5.xlarge",  
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",  
    "ServiceRole": "EMR_DefaultRole",
    "VisibleToAllUsers": True,
    "LogUri": "s3://project1-s3-dhivya/logs/", 
}

response = emr_client.run_job_flow(**cluster_params)
print(f"EMR Cluster Created! Cluster ID: {response['JobFlowId']}")
