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
from integrations.xml.scenarios import SCENARIOS


def generate_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def generate_hash(timestamp, merchant_id, order_id, amount, currency, card_number, secret):

    # Step 1 — build string with dots (as per docs)
    data = ".".join([
        timestamp,
        merchant_id,
        order_id,
        amount,
        currency,
        card_number
    ])
    # # debug
    # print("\nHASH STRING:")
    # print(data)

    # Step 2 — first hash
    hash1 = hashlib.sha1(data.encode("utf-8")).hexdigest()

    # Step 3 — final hash
    final_hash = hashlib.sha1(
        (hash1 + "." + secret).encode("utf-8")
    ).hexdigest()
    
    # # debug
    # print("\nHASH VALUE:")
    # print(final_hash)
    
    return final_hash



def build_xml():

    creds = load_credentials()
    
    # # debug
    # print("\nDEBUG CREDS:")
    # print(creds)
    # print("Merchant ID:", creds.get("merchant_id"))
    # print("Account ID:", creds.get("account_id"))

    timestamp = generate_timestamp()

    # Scenario selection
    if len(sys.argv) > 1:
        scenario_name = sys.argv[1]
    else:
        scenario_name = "success"

    scenario = SCENARIOS.get(scenario_name)

    if not scenario:
        raise ValueError(f"Scenario '{scenario_name}' not found")

    print(f"\nRunning scenario: {scenario_name}")

    # Load values from scenario
    order_id = scenario["order_id"]
    amount = scenario["amount"]
    currency = scenario["currency"]
    card_number = scenario["card_number"]

    hash_value = generate_hash(
    timestamp,
    creds["merchant_id"],
    order_id,
    amount,
    currency,
    card_number,
    creds["secret"]
)

    xml = f"""<request type="auth" timestamp="{timestamp}">
        <merchantid>{creds["merchant_id"]}</merchantid>
        <account>{creds["account_id"]}</account>
        <orderid>{order_id}</orderid>
        <amount currency="{currency}">{amount}</amount>
        <card>
            <number>{card_number}</number>
            <expdate>{scenario["expdate"]}</expdate>
            <chname>Luffy</chname>
            <type>{scenario["card_type"]}</type>
            <cvn>
                <number>{scenario["cvn"]}</number>
                <presind>1</presind>
            </cvn>
        </card>
        <autosettle flag="1"/>
        <sha1hash>{hash_value}</sha1hash>
    </request>"""

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