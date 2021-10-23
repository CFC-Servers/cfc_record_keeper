from boto3 import client as boto3_client
from os import environ
from json import dumps

response = {
    "statusCode": 204,
    "body": None
}

sns = boto3_client("sns")
topic = environ["CFCRecordTopic"]


def lambda_handler(event, context):

    sns.publish(
        TargetArn=topic,
        Message=dumps({"default": event["body"]}),
        MessageStructure="json"
    )

    return response
