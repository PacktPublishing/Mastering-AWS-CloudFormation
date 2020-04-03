import os
import boto3
import datetime as dt


def lambda_handler(event, context):

    parties_table = boto3.resource("dynamodb").Table(os.getenv("PARTIES_TABLE"))
    guests_table = boto3.resource("dynamodb").Table(os.getenv("GUESTS_TABLE"))
    s3 = boto3.client("s3")

    parties = parties_table.scan(
        AttributesToGet=["PartyName", "Date"]
    )['Items']

    for party in parties:
        party_date = dt.datetime.strptime(party['Date'], "%Y-%m-%d").date()
        if party_date > dt.date.today():
            guests = guests_table.scan(
                AttributesToGet=["GuestName", "Diet"],
                ScanFilter={
                    "PartyName": {
                        "AttributeValueList": [
                            party['PartyName']
                        ],
                        "ComparisonOperator": "EQ"
                    }
                }
            )['Items']
            party_doc = "---\n"
            party_doc += "Party Planning Report!!!\n"
            party_doc += f"Prepare for {party['PartyName']} on {party['Date']}!\n"
            party_doc += "Guests list:\n"
            for guest in guests:
                party_doc += f"- {guest['GuestName']} who is restricted to eat {guest['Diet']}\n"
            party_doc += "---\n"
            s3.put_object(
                Bucket=os.getenv("REPORTS_BUCKET"),
                Body=party_doc,
                Key=f"{party['PartyName']}.txt",
            )

    return {
        "statusCode": 200
    }
