SCENARIOS = {
    "success" : {
        "order_id" : "ORDER",
        "amount" : "33000",
        "currency" : "EUR",
        "card_number" : "4263970000005262",
        "expdate" : "1230",
        "cvn" : "125",
        "card_type" : "VISA",
        "expected_result": "00"
    },
    
    "wrong_cvn": {
    "order_id": "ORDER",
    "amount": "39000",
    "currency": "EUR",
    "card_number": "4263970000005262",
    "expdate": "1230",
    "cvn": "9999",   # wrong CVN
    "card_type": "VISA",
    "expected_result": "509"
},
    
    "invalid_hash": {
    "order_id": "ORDER",
    "amount": "33000",
    "currency": "EUR",
    "card_number": "4263970000005262",
    "expdate": "1230",
    "cvn": "125",
    "card_type": "VISA",
    "force_bad_hash": True,
    "expected_result": "505"
},
    "duplicate_order": {
    "order_id": "DUPLICATE_ORDER_TEST",
    "amount": "33000",
    "currency": "EUR",
    "card_number": "4263970000005262",
    "expdate": "1230",
    "cvn": "125",
    "card_type": "VISA",
    "expected_result": "501",
    "use_static_order_id": True
}
}
