from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Merchant Website Running"

@app.route("/pay", methods=["POST"])
def pay():

    data = request.json

    amount = data.get("amount")
    currency = data.get("currency")

    print("Payment requested:")
    print("Amount:", amount)
    print("Currency:", currency)

    return jsonify({
        "status": "payment received",
        "amount": amount,
        "currency": currency
    })

if __name__ == "__main__":
    app.run(debug=True)