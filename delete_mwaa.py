import boto3

def delete_mwaa_environment(environment_name):
    mwaa_client = boto3.client('mwaa')

    try:
        mwaa_client.delete_environment(Name=environment_name)
        print(f"MWAA Environment '{environment_name}' deletion initiated.")
    except Exception as e:
        print(f"Error deleting MWAA Environment: {e}")

# Replace with your MWAA environment name
delete_mwaa_environment("my-mwaa-env")
