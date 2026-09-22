import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


# FIXTURES

@pytest.fixture
def sample_transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 555555555,
            "state": "CANCELED",
            "date": "2023-01-12T11:00:00.123456",
            "operationAmount": {
                "amount": "1500.00",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Покупка в магазине",
            "to": "Счет 12345678901234567890"
        },
        {
            "id": 999999999,
            "state": "EXECUTED",
            "date": "2026-09-22T12:00:00.000000",
            # Тестовый случай без описания
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            }
        },
        {
            "id": 111111111,
            "state": "EXECUTED",
            # Имитация битой структуры без валюты для проверки try-except блока
            "operationAmount": {}
        }
    ]



# TEST filter_by_currency


def test_filter_by_currency_success(sample_transactions):
    """Проверка корректности фильтрации транзакций по заданной валюте"""
    usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
    assert len(usd_transactions) == 2
    assert usd_transactions[0]["id"] == 939719570
    assert usd_transactions[1]["id"] == 142264268


def test_filter_by_currency_rub(sample_transactions):
    """Проверка фильтрации по другой существующей валюте (RUB)"""
    rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
    assert len(rub_transactions) == 1
    assert rub_transactions[0]["id"] == 555555555


def test_filter_by_currency_no_match(sample_transactions):
    """Проверка случая, когда транзакции в заданной валюте отсутствуют (например, GBP)"""
    result = list(filter_by_currency(sample_transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_list():
    """Убеждаемся, что генератор не падает при обработке пустого списка"""
    result = list(filter_by_currency([], "USD"))
    assert result == []



#TEST transaction_descriptions


def test_transaction_descriptions_success(sample_transactions):
    """Проверка, что функция поочередно возвращает корректные описания"""
    descriptions = list(transaction_descriptions(sample_transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Покупка в магазине",
        "",  # Для транзакции 999999999 (отсутствует description)
        ""  # Для транзакции 111111111 (отсутствует description)
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty():
    """Тестирование работы с пустой входной структурой данных"""
    assert list(transaction_descriptions([])) == []



#TEST card_number_generator


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (0, 0, ["0000 0000 0000 0000"]),
        (9999999999999998, 9999999999999999, ["9999 9999 9999 9998", "9999 9999 9999 9999"])
    ]
)
def test_card_number_generator_ranges(start, end, expected):
    """Проверка диапазонов, граничных условий и корректного завершения генератора"""
    assert list(card_number_generator(start, end)) == expected


def test_card_number_generator_formatting():
    """Проверка правильности расстановки пробелов и общей длины номера карты"""
    generator = card_number_generator(123456, 123456)
    card_str = next(generator)

    assert len(card_str) == 19  # 16 цифр + 3 пробела
    assert card_str.count(" ") == 3
    assert card_str == "0000 0000 0012 3456"
