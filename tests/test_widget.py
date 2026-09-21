import pytest
from src.widget import mask_account_card, get_date


#фиктсуры для WIDGETS

@pytest.fixture
def widget_valid_card_numbers() -> list[tuple[str, str]]:
    """Корректные данные для mask_account_card."""
    return [
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ]


@pytest.fixture
def widget_invalid_card_numbers() -> list[tuple[str, str]]:
    """Некорректные данные для mask_account_card."""
    return [
        ("НеизвестныйТип 1234567812345678", "НеизвестныйТип 1234 56** **** 5678"),
        ("Visa Gold", "Visa Gold Некорректный номер карты"),
    ]


@pytest.fixture
def widget_correct_dates() -> list[tuple[str, str]]:
    """Корректные даты."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-01T00:00:00.000", "01.12.2023"),
        ("2025-01-05", "05.01.2025"),
    ]

# TESTS

@pytest.mark.parametrize(
    "index",
    [
        0,
        1,
        2,
    ],
)
def test_mask_account_card_valid(
    widget_valid_card_numbers: list[tuple[str, str]],
    index: int,
) -> None:
    """Проверяет маскирование карт и счетов."""
    input_data, expected = widget_valid_card_numbers[index]

    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "index",
    [
        0,
        1,
    ],
)
def test_mask_account_card_invalid(
    widget_invalid_card_numbers: list[tuple[str, str]],
    index: int,
) -> None:
    """Проверяет обработку некорректных данных."""
    input_data, expected = widget_invalid_card_numbers[index]

    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-01T00:00:00.000", "01.12.2023"),
        ("2025-01-05", "05.01.2025"),
    ],
)
def test_get_date_valid(date_string: str, expected: str) -> None:
    """Проверяет преобразование дат."""
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("11-03-2024", "03.20.11"),
        ("not-a-date", "a.-t.not"),
        ("", ".."),
    ],
)
def test_get_date_unusual(date_string: str, expected: str) -> None:
    """Проверяет работу функции с нестандартными строками."""
    assert get_date(date_string) == expected


def test_get_date_none() -> None:
    """Проверяет ошибку при передаче None."""
    with pytest.raises(TypeError):
        get_date(None)  # type: ignore[arg-type]


def test_mask_account_card_empty_string() -> None:
    """Проверяет ошибку при передаче пустой строки."""
    with pytest.raises(IndexError):
        mask_account_card("")


def test_mask_account_card_none() -> None:
    """Проверяет ошибку при передаче None."""
    with pytest.raises(AttributeError):
        mask_account_card(None)  # type: ignore[arg-type]

