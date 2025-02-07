import os
import boto3
import logging
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def create_bucket_ap_south_1(bucket_name):

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_DEFAULT_REGION', 'ap-south-1') 

    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    try:
        location = {'LocationConstraint': region_name}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        print(f"Bucket '{bucket_name}' created successfully in '{region_name}' region.")
        return True
    except ClientError as e:
        logging.error(e)
        print(f"Failed to create bucket: {e}")
        return False


if __name__ == "__main__":
    bucket_name = "project1-s3-dhivya"
    if create_bucket_ap_south_1(bucket_name):
        print("Bucket created successfully!")
    else:
        print("Bucket creation failed.")

