from base64 import b64decode
from lzma import decompress
from boto3 import client as boto3_client
from json import loads
from time import time

s3_client = boto3_client('s3')
bucket = "cfc-record-keeper"


def save_record(content, path):
    print(f"Saving {path}")

    s3_client.put_object(
        Body=content,
        Bucket="cfc-record-keeper",
        Key=path
    )


def decode_record(record):
    b64 = b64decode(record)
    raw = decompress(b64)

    return raw


def lambda_handler(event, context):
    print("Received data:")
    raw_data = event["Records"][0]["Sns"]["Message"]
    print(raw_data)
    data = loads(raw_data)
    print("-----")
    print(data)
    records = data.get("records", [])
    realm = data.get("realm", "unknown-realm")

    for record in records:
        name = record.get("name", "unknown-name")
        print(name)
        code = decode_record(record["compress"])
        spawn_time = record.get("spawnTime", round(time()))
        owner_steam_id = record.get("owner", "unattributed")
        includes = record.get("includes", [])

        save_prefix = f"records/{realm}/{owner_steam_id}/{spawn_time}-{name}"
        save_path = f"{save_prefix}.txt"
        save_record(code, save_path)

        for include in includes:
            include_name = include.get("name", "unknown-name")
            include_code = decode_record(include["compress"])

            save_path = f"{save_prefix}-includes/{include_name}.txt"
            save_record(include_code, save_path)
