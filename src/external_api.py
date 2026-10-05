import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def convert_currency(transaction: dict) -> float:
    amount = float(transaction["amount"])
    currency = transaction["currency"]

    if currency == "RUB":
        return amount

    url = "https://api.apilayer.com/exchangerates_data/latest"

    headers = {
        "apikey": API_KEY,
    }

    params = {
        "base": currency,
        "symbols": "RUB",
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    data = response.json()

    rate = data["rates"]["RUB"]

    return amount * rate


