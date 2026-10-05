import os
from typing import Any
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY: str = os.getenv("API_KEY") or ""


def convert_currency(transaction: dict[str, Any]) -> float:
    amount = float(transaction["amount"])
    currency = transaction["currency"]
    """Если валюта изначально рубли, то сразу возвращает сумму"""
    if currency == "RUB":
        return amount
    """Ссылка"""
    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {
        "apikey": API_KEY,
    }
    """Параметры"""
    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }
    """запрос"""
    response = requests.get(
        url,
        headers=headers,
        params=params,
    )

    data = response.json()


    return float(data["result"])
