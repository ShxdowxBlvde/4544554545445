from unittest.mock import patch


import src.external_api

@patch('src.external_api.requests.get')
def test_convert_usd_to_rub(mock_get):
    mock_get.return_value.json.return_value = {
        "rates": {
            "RUB": 90.0
        }
    }
    transaction = {
        "amount": 100,
        "currency": "USD"
    }
    amount = src.external_api.convert_currency(transaction)
    assert amount == 9000.0

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "USD", "symbols": "RUB"},
    )

@patch('src.external_api.requests.get')
def test_convert_rub(mock_get):
    transaction = {
        "amount": 5000.0,
        "currency": "RUB",
    }
    amount = src.external_api.convert_currency(transaction)
    assert amount == 5000.0
    mock_get.assert_not_called()

@patch('src.external_api.requests.get')
def test_convert_eur_to_rub(mock_get):
    mock_get.return_value.json.return_value = {
        "rates": {
            "RUB": 95.0
        }
    }
    transaction = {
        "amount": 100,
        "currency": "EUR",
    }
    amount = src.external_api.convert_currency(transaction)
    assert amount == 9500.0

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "EUR", "symbols": "RUB"},
    )

@patch('src.external_api.requests.get')
def test_convert_uses_rub_rate(mock_get):
    mock_get.return_value.json.return_value = {
        "rates": {
            "RUB": 90.0,
            "EUR": 0.92,
            "USD": 1.0,
            "GBP": 0.78,
        }
    }
    transaction = {
        "amount": 100,
        "currency": "USD",
    }

    amount = src.external_api.convert_currency(transaction)
    assert amount == 9000.0
    mock_get.assert_called_once()

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        headers={"apikey": src.external_api.API_KEY},
        params={"base": "USD", "symbols": "RUB"},
    )
