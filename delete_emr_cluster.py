import boto3
import os
from dotenv import load_dotenv

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_DEFAULT_REGION")
cluster_id = "j-XXXXXXXXXXXXX"  # Replace your cluster_id

emr_client = boto3.client(
    "emr",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)

try:
    response = emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
    print(f"EMR Cluster {cluster_id} is being terminated.")
except Exception as e:
    print(f"Failed to terminate cluster: {e}")
