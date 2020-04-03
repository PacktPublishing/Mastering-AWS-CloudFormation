import boto3


def check_if_key_exists():
    client = boto3.client('ec2')
    try:
        resp = client.describe_key_pairs(KeyNames=["mykey"])
    except Exception:
        return False
    if len(resp['KeyPairs']) == 0:
        return False
    return True


def check_if_core_stack_exists():
    client = boto3.client('cloudformation')
    try:
        resp = client.describe_stacks(StackName="core")
    except Exception:
        return False
    if len(resp['Stacks']) == 0:
        return False
    return True


def check_if_exports_exist():
    to_check = ["WebTierSubnet1Id",
                'WebTierSubnet2Id',
                "WebTierSubnet3Id",
                "VpcId",
                "WebTierMaxSizeParameter",
                "WebTierMinSizeParameter",
                "WebTierDesSizeParameter"]
    exports = []
    client = boto3.client('cloudformation')
    try:
        resp = client.list_exports()
    except Exception:
        return False
    for export in resp['Exports']:
        exports.append(export['Name'])
    if not all(exp in exports for exp in to_check):
        return False
    return True


def lambda_handler(event, context):
    status = "SUCCEEDED"
    if not (check_if_key_exists() and check_if_core_stack_exists() and check_if_exports_exist()):
        status = "FAILED"
    return {
        'Status': status
    }
