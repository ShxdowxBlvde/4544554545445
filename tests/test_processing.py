from unittest import result

import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_operations, process_bank_searching


# фикстуры для PROCESSING
@pytest.fixture
def search_transactions() -> list[dict[str, object]]:
    """Набор транзакций с описаниями для проверки process_bank_operations и process_bank_searching"""
    return [

            {"id": 1, "description": "Перевод организации"},
            {"id": 2, "description": "Оплата услуг: Мобильная связь"},
            {"id": 3, "description": "Перевод частному лицу"},
            {"id": 4, "description": "Покупка: Продукты супермаркет"},

    ]

@pytest.fixture
def processing_transactions() -> list[dict[str, object]]:
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
def processing_empty_transactions() -> list[dict[str, object]]:
    """Пустой список транзакций."""
    return []


# TESTS


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(
    processing_transactions: list[dict[str, object]],
    state: str,
    expected_ids: list[int],
) -> None:
    """Проверяет фильтрацию транзакций по статусу."""
    result = filter_by_state(
        processing_transactions,
        state,
    )

    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(
    processing_transactions: list[dict[str, object]],
) -> None:
    """Проверяет статус EXECUTED по умолчанию."""
    result = filter_by_state(processing_transactions)

    assert [item["id"] for item in result] == [1, 3]


def test_filter_by_state_empty(
    processing_empty_transactions: list[dict[str, object]],
) -> None:
    """Проверяет фильтрацию пустого списка."""
    assert filter_by_state(processing_empty_transactions) == []


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [
        (True, [4, 2, 1, 3]),
        (False, [3, 1, 2, 4]),
    ],
)
def test_sort_by_date(
    processing_transactions: list[dict[str, object]],
    reverse: bool,
    expected_ids: list[int],
) -> None:
    """Проверяет сортировку по датам."""
    result = sort_by_date(
        processing_transactions,
        reverse=reverse,
    )

    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_default(processing_transactions: list[dict[str, object]]) -> None:
    """Проверяет сортировку по убыванию по умолчанию."""
    result = sort_by_date(processing_transactions)

    assert [item["id"] for item in result] == [4, 2, 1, 3]


def test_sort_by_date_empty(
    processing_empty_transactions: list[dict[str, object]],
) -> None:
    """Проверяет сортировку пустого списка."""
    assert sort_by_date(processing_empty_transactions) == []


def test_sort_by_date_without_date() -> None:
    """Проверяет обработку отсутствующего ключа date."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01"},
    ]

    result = sort_by_date(data)

    assert result[0]["id"] == 2
    assert result[1]["id"] == 1

#тесты process_bank_operations

def test_process_bank_search_found(search_transactions: list[dict[str, object]]) -> None:
    """Тест успешной работы функции"""
    result = process_bank_searching(search_transactions, "Перевод")
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3

def test_process_bank_search_ignore_case(search_transactions: list[dict[str, object]]) -> None:
    """тест с игнорированием регистра"""
    result = process_bank_searching(search_transactions, "оплата")
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_process_bank_search_not_found(search_transactions: list[dict[str, object]]) -> None:
    """тест с отсутствующими операциями"""
    result = process_bank_searching(search_transactions, "Снятие наличных")
    assert result == []

def test_process_bank_search_miss_dscription(processing_transactions: list[dict[str, object]]) -> None:
    """тест со старой фикстурой"""
    result = process_bank_searching(processing_transactions, "Перевод")
    assert result == []

def test_process_bank_search_empty_data(processing_empty_transactions: list[dict[str, object]]) -> None:
    assert process_bank_searching(processing_empty_transactions, "Перевод") == []

#Тесты для process_bank_searching

def test_process_bank_operation_counting(search_transactions:list[dict[str, object]]) -> None:
    """Тест корректного подсчета количества операций по категориям"""
    categories = ["Перевод", "Оплата", "Продукты", "Снятие"]
    expected = {
        "Перевод": 2,
        "Оплата": 1,
        "Продукты": 1,
        "Снятие": 0
    }
    assert process_bank_operations(search_transactions, categories) == expected

def test_process_bank_operation_empty_categories(search_transactions:list[dict[str, object]]) -> None:
    """Тест передачи пустого списка"""
    assert process_bank_operations(search_transactions, []) == {}

def test_process_bank_operation_missing_description(
    search_transactions: list[dict[str, object]],
    processing_transactions: list[dict[str, object]]
    )-> None:
    """Тест подсчета на данных без поля description (используем вашу старую фикстуру)."""
    categories = ["Перевод", "Оплата"]
    expected = {"Перевод": 0, "Оплата": 0}
    assert process_bank_operations(processing_transactions, categories) == expected