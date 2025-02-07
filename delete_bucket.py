import os
import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

def empty_and_delete_bucket(bucket_name):
    """Deletes all objects in an S3 bucket and then deletes the bucket itself."""
    try:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = os.getenv('AWS_DEFAULT_REGION', 'ap-south-1')

        if not aws_access_key_id or not aws_secret_access_key:
            print("AWS credentials not found in environment variables.")
            return False

        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        print(f"Checking if bucket '{bucket_name}' exists...")

        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                print(f"Bucket '{bucket_name}' does not exist.")
                return False
            elif error_code == '403':
                print(f"Access denied to bucket '{bucket_name}'. Check permissions.")
                return False
            else:
                print(f"Unexpected error: {e}")
                return False

        bucket = s3_resource.Bucket(bucket_name)

        print(f"Emptying bucket '{bucket_name}'...")

        bucket.object_versions.delete()

        bucket.objects.delete()

        print(f"Deleting bucket '{bucket_name}'...")

        s3_client.delete_bucket(Bucket=bucket_name)

        print(f"Bucket '{bucket_name}' deleted successfully.")
        return True

    except NoCredentialsError:
        print("AWS credentials not found. Make sure you have configured them correctly.")
        return False

    except ClientError as e:
        logging.error(e)
        print(f"Failed to delete bucket: {e}")
        return False

if __name__ == "__main__":
    bucket_name = "project1-s3-dhivya"
    if empty_and_delete_bucket(bucket_name):
        print("Bucket deleted successfully!")
    else:
        print("Bucket deletion failed.")
