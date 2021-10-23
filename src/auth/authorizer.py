from os import getenv
from json import loads
from json.decoder import JSONDecodeError


def is_authorized(authorized):
    return {"isAuthorized": authorized}


def deny():
    return is_authorized(False)


def accept():
    return is_authorized(True)


def get_env(env_name):
    auth_config = {}
    try:
        if auth_config_string := getenv("JSON_ENV"):
            auth_config = loads(auth_config_string)
    except Exception as e:
        pass

    return getenv(env_name) or auth_config.get(env_name, None)


def get_allowed_keys(route):
    route = route.replace("/", "")
    route = route.replace("-", "_")
    route = route.upper()

    allowed_key_names = get_env(f"{route}_ALLOWED")

    if not allowed_key_names:
        return None

    allowed_keys = set()
    allowed_key_names = allowed_key_names.split(",")
    for key_name in allowed_key_names:
        key = get_env(key_name)

        if not key:
            print(f"Warning! Couldn't find key in environment: {key_name}")
            continue

        allowed_keys.add(key)

    return allowed_keys


def handler(event, context):
    key = event.get("headers", {}).get("authorization", None)

    if key is None:
        print("Auth is none, returning False")
        return deny()

    route = event.get("rawPath", None)

    if route is None:
        print("Route is none, returning False")
        return deny()

    allowed_keys = get_allowed_keys(route)

    if allowed_keys is None:
        print(f"Couldn't find any allowed keys for given route, '{route}'. Denying.")
        return deny()

    is_authorized = key in allowed_keys

    if is_authorized:
        return accept()

    return deny()
