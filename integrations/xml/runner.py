import os
import sys

# Allow importing project modules
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from integrations.xml.xml_client import send_request


if __name__ == "__main__":
    send_request()