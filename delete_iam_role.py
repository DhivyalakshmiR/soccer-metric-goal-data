import boto3

def delete_iam_role(role_name):
    iam_client = boto3.client('iam')

    try:
        # Detach all attached policies
        attached_policies = iam_client.list_attached_role_policies(RoleName=role_name)
        for policy in attached_policies['AttachedPolicies']:
            iam_client.detach_role_policy(RoleName=role_name, PolicyArn=policy['PolicyArn'])

        # Delete inline policies
        inline_policies = iam_client.list_role_policies(RoleName=role_name)
        for policy_name in inline_policies['PolicyNames']:
            iam_client.delete_role_policy(RoleName=role_name, PolicyName=policy_name)

        # Delete role
        iam_client.delete_role(RoleName=role_name)
        print(f"IAM Role '{role_name}' deleted successfully.")
    
    except Exception as e:
        print(f"Error deleting IAM Role: {e}")

# Replace with your IAM role names
delete_iam_role("EMR_EC2_DefaultRole")
delete_iam_role("EMR_DefaultRole")
