import boto3

image_names = {
    "amazonlinux2": "amzn2-ami-hvm-2.0.20191217.0-x86_64-gp2",
    "ubuntu": "ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-20200112",
    "rhel": "RHEL-8.0.0_HVM-20190618-x86_64-1-Hourly2-GP2",
    "sles": "suse-sles-15-sp1-v20191112-hvm-ssd-x86_64"
}


def get_image(img_name):
    client = boto3.client("ec2")
    resp = client.describe_images(Filters=[{"Name": "name",
                                     "Values": [img_name]}])
    return resp['Images'][0]['ImageId']


def lambda_handler(event, context):
    response = {}
    response['requestId'] = event['requestId']
    response['fragment'] = {"ImageId": ""}
    response['status'] = "SUCCESS"
    osfamily = event['params']['OSFamily']

    if osfamily not in image_names.keys():
        response['status'] = "FAILURE"
        return response

    image_id = get_image(image_names[osfamily])
    response['fragment']["ImageId"] = image_id
    return response