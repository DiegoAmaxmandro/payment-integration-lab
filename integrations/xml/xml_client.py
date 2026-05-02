import requests
import hashlib
import datetime
import os
import sys

# Allow importing config loader
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from merchant_system.config_loader import load_credentials


def generate_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def generate_hash(timestamp, merchant_id, order_id, amount, currency, secret):

    # First hash
    data = timestamp + merchant_id + order_id + amount + currency
    hash1 = hashlib.sha1(data.encode()).hexdigest()

    # Final hash
    final_hash = hashlib.sha1(
        (hash1 + secret).encode()
    ).hexdigest()

    return final_hash


def build_xml():

    creds = load_credentials()

    timestamp = generate_timestamp()

    order_id = "ORDER123"

    amount = "55000"  # 100 = €1.00
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

    <card>
        <number>4111111111111111</number>
        <expdate>1225</expdate>
        <chname>Test User</chname>
        <cvn>
            <number>123</number>
            <presind>1</presind>
        </cvn>
    </card>

    <autosettle flag="0"/>

    <sha1hash>{hash_value}</sha1hash>
</request>
"""

    return xml


def send_request():

    creds = load_credentials()

    url = creds["endpoint"]

    xml_payload = build_xml()

    print("\nSending request to:")
    print(url)

    response = requests.post(
        url,
        data=xml_payload,
        headers={
            "Content-Type": "text/xml"
        },
        timeout=30
    )

    print("\nStatus Code:", response.status_code)

    print("\nGateway Response:\n")
    print(response.text)


if __name__ == "__main__":

    send_request()