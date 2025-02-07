import boto3
from dotenv import load_dotenv
import os

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')

ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key_id,
                   aws_secret_access_key=aws_secret_access_key,
                   region_name=aws_region)

vpc = ec2.create_vpc(CidrBlock='192.168.0.0/16')
vpc_id = vpc['Vpc']['VpcId']
print(f"VPC Created with ID: {vpc_id}")

ec2.create_tags(Resources=[vpc_id], Tags=[{"Key": "Name", "Value": "my_vpc"}])

ig = ec2.create_internet_gateway()
ig_id = ig['InternetGateway']['InternetGatewayId']
ec2.attach_internet_gateway(InternetGatewayId=ig_id, VpcId=vpc_id)
print(f"Internet Gateway Created and Attached with ID: {ig_id}")

route_table = ec2.create_route_table(VpcId=vpc_id)
route_table_id = route_table['RouteTable']['RouteTableId']
ec2.create_route(
    RouteTableId=route_table_id,
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=ig_id
)
print(f"Route Table Created with ID: {route_table_id}")

subnet = ec2.create_subnet(CidrBlock='192.168.1.0/24', VpcId=vpc_id)
subnet_id = subnet['Subnet']['SubnetId']
print(f"Subnet Created with ID: {subnet_id}")

ec2.associate_route_table(RouteTableId=route_table_id, SubnetId=subnet_id)
print(f"Route Table Associated with Subnet ID: {subnet_id}")
