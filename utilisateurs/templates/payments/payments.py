# payments/stancer.py

import requests
import base64
from django.conf import settings

STANCER_API_KEY = settings.STANCER_PRIVATE_KEY  # pas besoin d'importer STANCER_PRIVATE_KEY directement
STANCER_BASE_URL = "https://api.stancer.com/v1"

def get_auth_header():
    auth = base64.b64encode(f"{STANCER_API_KEY}:".encode()).decode()
    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    }

def create_card(number, exp_month, exp_year, cvc):
    url = f"{STANCER_BASE_URL}/cards/"
    headers = get_auth_header()
    data = {
        "number": number,
        "exp_month": exp_month,
        "exp_year": exp_year,
        "cvc": cvc,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_payment(amount, card_id):
    url = f"{STANCER_BASE_URL}/payment"
    headers = get_auth_header()
    data = {
        "amount": amount,
        "currency": "eur",
        "card": card_id,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
