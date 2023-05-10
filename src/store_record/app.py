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


def save_record(content, path):
    print(f"Saving {path}")

    s3_client.put_object(
        Body=content,
        Bucket="cfc-record-keeper",
        Key=path
    )


def decode_record(record):
    b64 = base64.b64decode(record)
    raw = lzma.decompress(b64)

    return raw


def lambda_handler(event, context):
    data = json.loads(event["body"])
    records = data.get("records", [])
    realm = data.get("realm", "unknown-realm")

    for record in records:
        name = record.get("name", "unknown-name")
        code = decode_record(record["compress"])
        spawn_time = record.get("spawnTime", round(time.time()))
        owner_steam_id = record.get("owner", "unattributed")
        includes = record.get("includes")

        save_prefix = f"records/{realm}/{owner_steam_id}/{spawn_time}-{name}"
        save_path = f"{save_prefix}.txt"
        save_record(code, save_path)

        for include in includes:
            include_name = include.get("name", "unknown-name")
            include_code = decode_record(include["compress"])

            save_path = f"{save_prefix}-includes/{include_name}.txt"
            save_record(include_code, save_path)

    return response
