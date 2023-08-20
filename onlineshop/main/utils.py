import requests
from decouple import config

PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY")


def initialize_transaction(email, amount, card_number, expiration_month, expiration_year, cvc):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "amount": str(amount),
        "currency": "KES",
        "card": {
            "number": card_number,
            "cvv": cvc,
            "expiry_month": expiration_month,
            "expiry_year": expiration_year
        }
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    return response_data


def verify_transaction(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"{PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    return response.json()

