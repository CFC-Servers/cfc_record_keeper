import base64
import boto3
import json
import lzma
import time

response = {
    "statusCode": 204,
    "body": None
}

s3_client = boto3.client('s3')
bucket = "cfc-record-keeper"

def decode_record(record):
    b64 = base64.b64decode(record)
    raw = lzma.decompress(b64)

    return raw

def lambda_handler(event, context):
    data = json.loads(event["body"])

    name = data.get("name", "unknown-name").upper()
    record = decode_record(data["compress"])
    realm = data.get("realm", "unknown-realm")
    spawn_time = data.get("spawnTime", round(time.time()))
    owner_steam_id = data.get("owner", "unattributed").lower()

    save_path = f"records/{realm}/{owner_steam_id}/{name}-{spawn_time}.txt"
    print(f"Saving {save_path}")

    s3_client.put_object(Body=record, Bucket="cfc-record-keeper", Key=save_path)

    return response
