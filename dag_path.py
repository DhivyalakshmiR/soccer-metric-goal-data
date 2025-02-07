import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get S3 bucket name from .env file
s3_client = boto3.client("s3")
bucket_name = os.getenv("S3_BUCKET_NAME", "project1-s3-dhivya")
dag_file_path = "dags/my_dag.py"  # Local path of DAG file
s3_dag_path = "dags/my_dag.py"  # Destination in S3

# Ensure bucket exists
try:
    s3_client.head_bucket(Bucket=bucket_name)
    print(f"✅ S3 bucket '{bucket_name}' exists.")
except Exception:
    print(f"❌ S3 bucket '{bucket_name}' not found. Creating it now...")
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"✅ S3 bucket '{bucket_name}' created.")

# Upload DAG file
try:
    s3_client.upload_file(dag_file_path, bucket_name, s3_dag_path)
    print(f"✅ Uploaded '{dag_file_path}' to 's3://{bucket_name}/{s3_dag_path}'")
except Exception as e:
    print(f"❌ Error uploading DAG: {e}")
