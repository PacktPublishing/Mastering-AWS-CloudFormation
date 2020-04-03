import boto3
import botocore
import sys

matches = []

try:
    stack = sys.argv[1]
except IndexError:
    print("Please provide a stack name")
    sys.exit(1)

cfn_client = boto3.client('cloudformation')

try:
    resources = cfn_client.describe_stack_resources(StackName=stack)
except botocore.exceptions.ClientError:
    print("This stack does not exist or region is incorrect")
    sys.exit(1)

subnets_in_stack = []
for resource in resources['StackResources']:
    if resource['LogicalResourceId'] == "PrivateRouteTable":
        private_route_table = resource['PhysicalResourceId']
    if resource['ResourceType'] == "AWS::EC2::Subnet":
        subnets_in_stack.append(resource['PhysicalResourceId'])

ec2_client = boto3.client('ec2')
subnets_to_check = []
for subnet in subnets_in_stack:
    resp = ec2_client.describe_subnets(SubnetIds=[subnet])
    for tag in resp['Subnets'][0]['Tags']:
        if tag['Key'] == "Private" and tag['Value'] == "True":
            subnets_to_check.append(subnet)

route_table = ec2_client.describe_route_tables(RouteTableIds=[private_route_table])
private_subnets = []
for assoc in route_table['RouteTables'][0]['Associations']:
    private_subnets.append(assoc['SubnetId'])

for subnet in subnets_to_check:
    if subnet not in private_subnets:
        matches.append(subnet)

if matches:
    print("One or more private subnets are not associated with proper route table!")
    print(f"Non-compliant subnets: {matches}")
    sys.exit(1)

print("All subnets are compliant!")
exit(0)
