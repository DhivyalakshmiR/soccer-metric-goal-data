import boto3

def delete_vpc(vpc_id):
    ec2 = boto3.resource('ec2')
    vpc = ec2.Vpc(vpc_id)

    try:
        for igw in vpc.internet_gateways.all():
            vpc.detach_internet_gateway(InternetGatewayId=igw.id)
            igw.delete()

        for subnet in vpc.subnets.all():
            subnet.delete()

        for sg in vpc.security_groups.all():
            if sg.group_name != 'default':
                sg.delete()

        for rt in vpc.route_tables.all():
            if not rt.associations:
                rt.delete()

        vpc.delete()
        print(f"VPC '{vpc_id}' deleted successfully.")
    
    except Exception as e:
        print(f"Error deleting VPC: {e}")

delete_vpc("vpc-XXXXXXXX")  # Replace your VPC ID
