import os
import datetime


def log_result(scenario_name, order_id, expected_result, actual_result, status):
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "xml_scenario_results.log")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = (
        f"{timestamp} | "
        f"scenario={scenario_name} | "
        f"order_id={order_id} | "
        f"expected={expected_result} | "
        f"actual={actual_result} | "
        f"status={status}\n"
    )

    with open(log_file, "a") as file:
        file.write(line)