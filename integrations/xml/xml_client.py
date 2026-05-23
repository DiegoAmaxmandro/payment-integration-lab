import requests
import hashlib
import datetime
import os
import sys
import time
import xml.etree.ElementTree as ET

# Allow importing config loader
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)
from merchant_system.config_loader import load_credentials
from integrations.xml.scenarios import SCENARIOS
from integrations.xml.logger import log_result


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
    
    # Step 2 — first hash
    hash1 = hashlib.sha1(data.encode("utf-8")).hexdigest()

    # Step 3 — final hash
    final_hash = hashlib.sha1(
        (hash1 + "." + secret).encode("utf-8")
    ).hexdigest()
    
    return final_hash

def build_xml(scenario_name):

    creds = load_credentials()
    timestamp = generate_timestamp()
    scenario = SCENARIOS.get(scenario_name)

    if not scenario:
        raise ValueError(f"Scenario '{scenario_name}' not found")

    print(f"\nRunning scenario: {scenario_name}")

    # Load values from scenario
    
    if scenario.get("use_static_order_id"):
        order_id = scenario["order_id"]
    else:
        order_id = f"{scenario['order_id']}_{int(time.time())}"
        
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
    if scenario.get("force_bad_hash"):
        hash_value = "0000000000000000000000000000000000000000"

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

    return xml, scenario, scenario_name, order_id

def send_request(scenario_name="success"):

    creds = load_credentials()
    url = creds["endpoint"]
    xml_payload, scenario, scenario_name, order_id = build_xml(scenario_name)
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
    root = ET.fromstring(response.text)
    actual_result = root.findtext("result")
    expected_result = scenario.get("expected_result")
    print("\nValidation:")
    print("Expected:", expected_result)
    print("Actual:", actual_result)

    if actual_result == expected_result:
        status = "PASSED"
    else:
        status = "FAILED"

    print("Scenario status:", status)

    log_result(
        scenario_name,
        order_id,
        expected_result,
        actual_result,
        status
    )

if __name__ == "__main__":

    send_request()