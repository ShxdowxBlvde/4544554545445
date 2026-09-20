import pytest

from masks import get_mask_card_number, get_mask_account
from widget import mask_account_card, get_date
from processing import filter_by_state, sort_by_date



# ФИКСТУРЫ


@pytest.fixture
def masks_valid_card_numbers():
    """Корректные номера карт."""
    return [
        "7000792289606361",
        "1234567812345678",
        "7000 7922 8960 6361",
    ]


@pytest.fixture
def masks_invalid_card_numbers():
    """Некорректные номера карт."""
    return [
        "1234",
        "",
        "123456789012345",
        "12345678901234567",
        "123456789012abcd",
    ]


@pytest.fixture
def masks_valid_account_numbers():
    """Корректные номера счетов."""
    return [
        "73654108430135874305",
        "12345678",
        "1234",
    ]


@pytest.fixture
def masks_invalid_account_numbers():
    """Некорректные номера счетов."""
    return [
        "123",
        "",
        "1234abcd",
    ]


@pytest.fixture
def widget_valid_card_numbers():
    """Корректные данные для mask_account_card."""
    return [
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]


@pytest.fixture
def widget_invalid_card_numbers():
    """Некорректные данные для mask_account_card."""
    return [
        ("НеизвестныйТип 1234567812345678",
         "НеизвестныйТип 1234 56** **** 5678"),
        ("Visa Gold", "Visa Gold Некорректный номер карты"),
    ]


@pytest.fixture
def widget_correct_dates():
    """Корректные даты."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-01T00:00:00.000", "01.12.2023"),
        ("2025-01-05", "05.01.2025"),
    ]


@pytest.fixture
def processing_transactions():
    """Набор транзакций для filter_by_state и sort_by_date."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-12-05T12:00:00.000",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-01T00:00:00.000",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2023-11-20T15:30:00.000",
        },
        {
            "id": 4,
            "state": "PENDING",
            "date": "2024-02-01T00:00:00.000",
        },
    ]


@pytest.fixture
def processing_empty_transactions():
    """Пустой список транзакций."""
    return []


