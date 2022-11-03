from json import dumps


def lambda_handler(event, context):
    print(event)
    print("")

    print(dumps(event, sort_keys=True, indent=4))
