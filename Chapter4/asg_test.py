from time import sleep
import boto3
import botocore
import requests
import sys

try:
    stack = sys.argv[1]
except IndexError:
    print("Please provide a stack name")
    sys.exit(1)

cfn_client = boto3.client('cloudformation')

try:
    stack = cfn_client.describe_stacks(StackName=stack)
except botocore.exceptions.ClientError:
    print("This stack does not exist or region is incorrect")
    sys.exit(1)

elb_dns = stack['Stacks'][0]['Outputs'][0]['OutputValue']
for _ in range(0, 2):
    resp = requests.get(f"http://{elb_dns}")
    if resp.status_code == 200:
        print("Test succeeded")
        sys.exit(0)
    sleep(5)

print(f"Result of test: {resp.content}")
print(f"HTTP Response code: {resp.status_code}")
print("Test did not succeed")
sys.exit(1)
