import requests
import json
import os
import sys

# Allow importing from merchant_system
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from merchant_system.config_loader import load_credentials


def create_headers(creds):

    headers = {
        "Content-Type": "application/json",
        "app_id": creds["app_id"],
        "app_key": creds["app_key"]
    }

    return headers


def test_connection():

    creds = load_credentials()

    headers = create_headers(creds)

    url = creds["endpoint"]

    print("Testing connection to sandbox...")
    print("Endpoint:", url)

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print("Status Code:", response.status_code)

        if response.status_code == 200:

            print("Connection successful")

        else:

            print("Connection failed")
            print("Response:", response.text)

    except requests.exceptions.RequestException as e:

        print("Error connecting to API:")
        print(str(e))


if __name__ == "__main__":

    test_connection()