from dotenv import load_dotenv
import os
import boto3

load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

s3 = boto3.client("s3")

def list_s3_buckets():
    try:
        response = s3.list_buckets()

        print("List of S3 Buckets:")
        for bucket in response["Buckets"]:
            print(f"- {bucket['Name']}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

list_s3_buckets()
