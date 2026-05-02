import json
import os


def load_credentials():

    # Build path to config file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(
        base_dir,
        "..",
        "config",
        "sandbox_credentials.json"
    )

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Credentials file not found: {config_path}"
        )

    with open(config_path, "r") as file:
        credentials = json.load(file)

    return credentials


def validate_credentials(creds):

    required_fields = [
        "environment",
        "endpoint",
        "app_id",
        "app_key",
        "merchant_id"
    ]

    missing = []

    for field in required_fields:
        if field not in creds or not creds[field]:
            missing.append(field)

    if missing:
        raise ValueError(
            f"Missing required credentials: {missing}"
        )


if __name__ == "__main__":

    creds = load_credentials()

    validate_credentials(creds)

    print("Credentials loaded successfully")
    print("Environment:", creds["environment"])
    print("Endpoint:", creds["endpoint"])
    print("Merchant ID:", creds["merchant_id"])