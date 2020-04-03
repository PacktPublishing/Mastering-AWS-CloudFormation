import boto3
import os
import json


def lambda_handler(event, context):
    parties_table = os.getenv("PARTIES_TABLE")
    guests_table = os.getenv("GUESTS_TABLE")
    dynamo_client = boto3.client("dynamodb")
    print(event)
    body = json.loads(event['body'])
    resp = dynamo_client.get_item(
        TableName=parties_table,
        Key={
            "PartyName":
                {"S": body["PartyName"]}
        }
    )
    if "Item" not in resp:
        dynamo_client.put_item(
            TableName=parties_table,
            Item={
                "PartyName":
                    {"S": body["PartyName"]},
                "Date":
                    {"S": body["PartyDate"]}
            }
        )
    dynamo_client.put_item(
        TableName=guests_table,
        Item={
            "GuestName":
                {"S": body["GuestName"]},
            "Diet":
                {"S": body["GuestDiet"]},
            "PartyName":
                {"S": body["PartyName"]}
        }
    )
    return {
        "statusCode": 200
    }
