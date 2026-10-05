from unittest.mock import Mock, patch
from typing import Any
import pytest
import src.external_api

"""Тест конвертирования долларов в рубли"""


@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"result": 9000.0}

    transaction: dict[str, Any] = {
        "amount": 100.0,
        "currency": "USD",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 9000.0

    """Проверка того, что происходит только один запрос"""
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": src.external_api.API_KEY},
        params={"from": "USD", "to": "RUB", "amount": 100.0},
    )


"""Проверка того, что если валюта - рубль, запрос не происходит"""


@patch("src.external_api.requests.get")
def test_convert_rub(mock_get: Mock) -> None:
    transaction: dict[str, float | str] = {
        "amount": 5000.0,
        "currency": "RUB",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 5000.0
    mock_get.assert_not_called()


"""Проверка корректности работы с euro"""


@patch("src.external_api.requests.get")
def test_convert_eur_to_rub(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"result": 9500.0}

    transaction: dict[str, Any] = {
        "amount": 100.0,
        "currency": "EUR",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 9500.0

    """Проверка, что происходит только один запрос"""
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": src.external_api.API_KEY},
        params={"from": "EUR", "to": "RUB", "amount": 100.0},
    )


"""Проверка с несколькими валютами"""


@pytest.mark.parametrize(
    "currency, amount, expected",
    [
        ("USD", 100.0, 9000.0),
        ("EUR", 100.0, 9500.0),
        ("GBP", 100.0, 12000.0),
    ],
)

@patch("src.external_api.requests.get")
def test_convert_currencies(
    mock_get: Mock,
    currency: str,
    amount: float,
    expected: float,
) -> None:
    mock_get.return_value.json.return_value = {
        "result": expected
    }

    transaction: dict[str, Any] = {
        "amount": amount,
        "currency": currency,
    }

    result: float = src.external_api.convert_currency(transaction)

    assert  result == expected

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": src.external_api.API_KEY},
        params={"from": currency,
                "to": "RUB",
                "amount": amount,
                },
    )
