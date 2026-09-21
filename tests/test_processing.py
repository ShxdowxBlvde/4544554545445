import pytest

from src.processing import filter_by_state, sort_by_date

# фикстуры для PROCESSING

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
