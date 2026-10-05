from unittest.mock import Mock, patch

import src.external_api

"""Тест конвертирования долларов в рубли"""


@patch("src.external_api.requests.get")
def test_convert_usd_to_rub(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}

    transaction: dict[str, int | str] = {
        "amount": 100,
        "currency": "USD",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 9000.0

    """Проверка того, что происходит только один запрос"""
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "USD", "symbols": "RUB"},
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
    mock_get.return_value.json.return_value = {"rates": {"RUB": 95.0}}

    transaction: dict[str, int | str] = {
        "amount": 100,
        "currency": "EUR",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 9500.0

    """Проверка, что происходит только один запрос"""
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "EUR", "symbols": "RUB"},
    )


"""Проверка с несколькими валютами"""


@patch("src.external_api.requests.get")
def test_convert_uses_rub_rate(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {
        "rates": {
            "RUB": 90.0,
            "EUR": 0.92,
            "USD": 1.0,
            "GBP": 0.78,
        }
    }

    transaction: dict[str, int | str] = {
        "amount": 100,
        "currency": "USD",
    }

    amount: float = src.external_api.convert_currency(transaction)

    assert amount == 9000.0

    mock_get.assert_called_once()

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "USD", "symbols": "RUB"},
    )
