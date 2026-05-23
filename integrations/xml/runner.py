import os
import sys

# Allow importing project modules
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../")
    )
)

from integrations.xml.xml_client import send_request
from integrations.xml.scenarios import SCENARIOS


def show_available_scenarios():
    print("\nAvailable scenarios:")

    for scenario_name in SCENARIOS.keys():
        print(f"- {scenario_name}")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        scenario_name = sys.argv[1]
    else:
        print("\nNo scenario provided.")
        show_available_scenarios()
        sys.exit(0)

    if scenario_name not in SCENARIOS:
        print(f"\nScenario '{scenario_name}' not found.")
        show_available_scenarios()
        sys.exit(1)

    send_request(scenario_name)