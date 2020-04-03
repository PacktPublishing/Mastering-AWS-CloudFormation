import requests
import json
import pymysql
import sys

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def create_db(dbname, dbuser, dbpassword, rdsendpoint, rdsuser, rdspassword):
    create_db_query = f"CREATE DATABASE {dbname};"
    create_user_query = f"CREATE USER '{dbuser}'@'%' IDENTIFIED BY '{dbpassword}';"
    grant_query = f"GRANT ALL PRIVILEGES ON {dbname}.* TO '{dbuser}'@'%';"
    flush_query = "FLUSH PRIVILEGES;"
    try:
        conn = pymysql.connect(host=rdsendpoint,
                               user=rdsuser,
                               password=rdspassword)
        cursor = conn.cursor()
        cursor.execute(create_db_query)
        cursor.execute(create_user_query)
        cursor.execute(grant_query)
        cursor.execute(flush_query)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as err:
        return err
    return None


def delete_db(dbname, dbuser, rdsendpoint, rdsuser, rdspassword):
    delete_db_query = f"DROP DATABASE {dbname}"
    delete_user_query = f"DROP USER '{dbuser}'"
    db_exists_query = f"SHOW DATABASES LIKE '{dbname}'"
    user_exists_query = f"SELECT user FROM mysql.user where user='{dbuser}'"
    try:
        conn = pymysql.connect(host=rdsendpoint,
                               user=rdsuser,
                               password=rdspassword)
        cursor = conn.cursor()
        db_exists = cursor.execute(db_exists_query)
        if db_exists:
            cursor.execute(delete_db_query)
        user_exists = cursor.execute(user_exists_query)
        if user_exists:
            cursor.execute(delete_user_query)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as err:
        return err
    return None


def handler(event, context):
    input_props = event['ResourceProperties']
    required_props = ["DBName", "RDSEndpoint", "RDSUser", "RDSPassword"]
    missing_props = [prop for prop in required_props if prop not in input_props]
    if missing_props:
        if event['RequestType'] == "Delete":
            send(event, context, SUCCESS, responseData={})
            sys.exit(0)
        reason = f"Required properties are missing: {missing_props}"
        send(event, context, FAILED, responseReason=reason, responseData={})
        sys.exit(1)
    db_name = input_props['DBName']
    rds_endpoint = input_props['RDSEndpoint']
    rds_user = input_props['RDSUser']
    rds_password = input_props['RDSPassword']

    if "DBUser" not in input_props or len(input_props['DBUser']) == 0:
        db_user = db_name
    else:
        db_user = input_props['DBUser']
    if "DBPassword" not in input_props or len(input_props['DBPassword']) == 0:
        db_password = db_name
    else:
        db_password = input_props['DBPassword']

    if event['RequestType'] == "Delete":
        err = delete_db(db_name, db_user, rds_endpoint, rds_user, rds_password)
    elif event['RequestType'] in ["Create", "Update"]:
        err = create_db(db_name, db_user, db_password, rds_endpoint, rds_user, rds_password)

    if err:
        print(err)
        send(event, context, FAILED, physicalResourceId="", responseData={})
        sys.exit(1)
    send(event, context, SUCCESS, physicalResourceId=db_name, responseData={})


def send(event, context, responseStatus, responseData, responseReason="", physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = responseReason
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))
