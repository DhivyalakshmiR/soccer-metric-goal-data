import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS credentials & config from .env file
aws_region = os.getenv("AWS_DEFAULT_REGION", "ap-south-1")
mwaa_env_name = os.getenv("MWAA_ENV_NAME", "MyAirflowEnvironment")
s3_bucket_name = os.getenv("S3_BUCKET_NAME", "project1-s3-dhivya")
execution_role_arn = os.getenv("MWAA_EXECUTION_ROLE", "arn:aws:iam::014498630942:role/MWAAExecutionRole")

# List of Subnet IDs and Security Group IDs from .env
subnet_ids = os.getenv("SUBNET_IDS").split(",")  # Example: "subnet-abc123,subnet-def456"
security_group_ids = os.getenv("SECURITY_GROUP_IDS").split(",")  # Example: "sg-xyz789"

# Initialize MWAA Boto3 client
mwaa_client = boto3.client("mwaa", region_name=aws_region)

# Create MWAA environment
try:
    response = mwaa_client.create_environment(
        Name=mwaa_env_name,
        ExecutionRoleArn=execution_role_arn,
        SourceBucketArn=f"arn:aws:s3:::{s3_bucket_name}",
        AirflowVersion="2.7.2",  # Choose appropriate version
        EnvironmentClass="mw1.small",  # Change to mw1.medium or mw1.large if needed
        MaxWorkers=5,
        MinWorkers=1,
        NetworkConfiguration={
            "SubnetIds": subnet_ids,
            "SecurityGroupIds": security_group_ids
        },
        WebserverAccessMode="PUBLIC_ONLY",  # Set to PRIVATE_ONLY if using a private VPC
        LoggingConfiguration={
            "DagProcessingLogs": {"Enabled": True, "LogLevel": "INFO"},
            "TaskLogs": {"Enabled": True, "LogLevel": "INFO"},
            "WebserverLogs": {"Enabled": True, "LogLevel": "INFO"},
            "SchedulerLogs": {"Enabled": True, "LogLevel": "INFO"},
            "WorkerLogs": {"Enabled": True, "LogLevel": "INFO"}
        },
        KmsKey="alias/aws/mwaa"  # Default KMS key, update if using a custom key
    )

    print("✅ MWAA Environment creation started successfully!")
    print("📌 Environment ARN:", response["Arn"])

except mwaa_client.exceptions.AccessDeniedException as e:
    print("❌ Access Denied: Check IAM permissions →", str(e))
except mwaa_client.exceptions.ValidationException as e:
    print("❌ Validation Error: Check input parameters →", str(e))
except Exception as e:
    print("❌ Unexpected error:", str(e))
