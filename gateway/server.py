from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/process-payment", methods=["POST"])
def process_payment():

    data = request.json

    amount = data.get("amount")
    currency = data.get("currency")
    card_number = data.get("card_number")

    print("Gateway received payment:")
    print("Amount:", amount)
    print("Currency:", currency)
    print("Card:", card_number)

    # Simulate random payment result
    outcome = random.choice([
        "approved",
        "declined",
        "error"
    ])

    if outcome == "approved":

        return jsonify({
            "status": "approved",
            "transaction_id": "TXN123456"
        })

    elif outcome == "declined":

        return jsonify({
            "status": "declined",
            "reason": "insufficient_funds"
        }), 402

    else:

        return jsonify({
            "status": "error",
            "message": "gateway timeout"
        }), 500


if __name__ == "__main__":
    app.run(port=5001, debug=True)