import pandas as pd
from unittest.mock import patch, MagicMock
from src.readers import read_csv_transactions, read_xlsx_transactions

"""
ТЕСТИРОВАНИЕ ФУНКЦИИ ЧТЕНИЯ CSV ФАЙЛОВ С КОРРЕКТНЫМИ ДАННЫМИ
"""


@patch("pandas.read_csv")
def test_read_csv_transactions(mock_read_csv:MagicMock) -> None:
    mock_df = pd.DataFrame(
        [
            {
                "id": 650703.0,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210.0,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
        ]
    )
    mock_read_csv.return_value = mock_df
    result = read_csv_transactions("fake_path.csv")
    mock_read_csv.assert_called_with("fake_path.csv", sep=";")

    assert result == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
    ]


"""
ТЕСТИРОВАНИЕ ФУНКЦИИ ЧТЕНИЯ CSV ФАЙЛОВ С AMOUNT = "NAN
"""


@patch("pandas.read_csv")
def test_read_csv_transactions_with_nan(mock_read_csv:MagicMock) -> None:
    mock_df = pd.DataFrame(
        [
            {
                "id": 3598919.0,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": float("nan"),
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            }
        ]
    )
    mock_read_csv.return_value = mock_df
    result = read_csv_transactions("fake_path_nan.csv")
    mock_read_csv.assert_called_with("fake_path_nan.csv", sep=";")
    assert result == [
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": "",
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        }
    ]


"""
ТЕСТИРОВАНИЕ ФУНКЦИИ ЧТЕНИЯ XLSX ФАЙЛОВ С КОРРЕКТНЫМИ ДАННЫМИ
"""


@patch("pandas.read_excel")
def test_read_xlsx_transactions(mock_read_excel:MagicMock) -> None:
    mock_df = pd.DataFrame(
        [
            {
                "id": 650703.0,
                "state": "EXECUTED",
                "date": "2023-09-05T11:30:32Z",
                "amount": 16210.0,
                "currency_name": "Sol",
                "currency_code": "PEN",
                "from": "Счет 58803664561298323391",
                "to": "Счет 39745660563456619397",
                "description": "Перевод организации",
            },
        ]
    )
    mock_read_excel.return_value = mock_df
    result = read_xlsx_transactions("fake_path.csv")
    mock_read_excel.assert_called_with("fake_path.csv", engine="openpyxl")
    assert result == [
        {
            "id": 650703.0,
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210.0,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
    ]


"""
ТЕСТИРОВАНИЕ ФУНКЦИИ ЧТЕНИЯ XLSX ФАЙЛОВ С AMOUNT = "NAN
"""


@patch("pandas.read_excel")
def test_read_xlsx_transactions_with_nan(mock_read_excel:MagicMock) -> None:
    mock_df = pd.DataFrame(
        [
            {
                "id": 3598919.0,
                "state": "EXECUTED",
                "date": "2020-12-06T23:00:58Z",
                "amount": float("nan"),
                "currency_name": "Peso",
                "currency_code": "COP",
                "from": "Discover 3172601889670065",
                "to": "Discover 0720428384694643",
                "description": "Перевод с карты на карту",
            }
        ]
    )
    mock_read_excel.return_value = mock_df
    result = read_xlsx_transactions("fake_path_nan.csv")
    mock_read_excel.assert_called_with("fake_path_nan.csv", engine="openpyxl")
    assert result == [
        {
            "id": 3598919.0,
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": "",
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        }
    ]
