import requests
import hashlib
import datetime
import os
import sys

# allow import from merchant_system
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from merchant_system.config_loader import load_credentials


def generate_timestamp():

    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def generate_hash(timestamp, merchant_id, order_id, amount, currency, secret):

    data = (
        timestamp +
        merchant_id +
        order_id +
        amount +
        currency
    )

    hash1 = hashlib.sha1(data.encode()).hexdigest()

    final_hash = hashlib.sha1(
        (hash1 + secret).encode()
    ).hexdigest()

    return final_hash


def create_xml_request():

    creds = load_credentials()

    timestamp = generate_timestamp()

    order_id = "ORDER123"

    amount = "100"

    currency = "EUR"

    hash_value = generate_hash(
        timestamp,
        creds["merchant_id"],
        order_id,
        amount,
        currency,
        creds["secret"]
    )

    xml = f"""
    <request type="auth">
        <merchantid>{creds["merchant_id"]}</merchantid>
        <account>{creds["account_id"]}</account>
        <orderid>{order_id}</orderid>
        <amount currency="{currency}">{amount}</amount>
        <timestamp>{timestamp}</timestamp>
        <sha1hash>{hash_value}</sha1hash>
    </request>
    """

    return xml


def send_request():

    creds = load_credentials()

    url = creds["endpoint"]

    xml_payload = create_xml_request()

    print("Sending XML request to:")
    print(url)

    response = requests.post(
        url,
        data=xml_payload,
        headers={
            "Content-Type": "text/xml"
        },
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)


if __name__ == "__main__":

    send_request()