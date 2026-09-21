import pytest

from src.masks import get_mask_card_number, get_mask_account
#фикстуры для masks
@pytest.fixture
def masks_valid_card_numbers() -> list[str]:
    """Корректные номера карт."""
    return [
        "7000792289606361",
        "1234567812345678",
        "7000 7922 8960 6361",
    ]


@pytest.fixture
def masks_invalid_card_numbers() -> list[str]:
    """Некорректные номера карт."""
    return [
        "1234",
        "",
        "123456789012345",
        "12345678901234567",
        "123456789012abcd",
    ]


@pytest.fixture
def masks_valid_account_numbers() -> list[str]:
    """Корректные номера счетов."""
    return [
        "73654108430135874305",
        "12345678",
        "1234",
    ]


@pytest.fixture
def masks_invalid_account_numbers() -> list[str]:
    """Некорректные номера счетов."""
    return [
        "123",
        "",
        "1234abcd",
    ]
# TESTS


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "7000 79** **** 6361"),
        (1, "1234 56** **** 5678"),
        (2, "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_valid(
    masks_valid_card_numbers: list[str],
    index: int,
    expected: str,
) -> None:
    """Проверяет корректное маскирование номеров карт."""
    assert get_mask_card_number(masks_valid_card_numbers[index]) == expected


@pytest.mark.parametrize(
    "index",
    [
        0,
        1,
        2,
        3,
        4,
    ],
)
def test_get_mask_card_number_invalid(
    masks_invalid_card_numbers: list[str],
    index: int,
) -> None:
    """Проверяет обработку некорректных номеров карт."""
    assert (
        get_mask_card_number(masks_invalid_card_numbers[index])
        == "Некорректный номер карты"
    )


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "**4305"),
        (1, "**5678"),
        (2, "**1234"),
    ],
)
def test_get_mask_account_valid(
    masks_valid_account_numbers: list[str],
    index: int,
    expected: str,
) -> None:
    """Проверяет корректное маскирование счетов."""
    assert get_mask_account(masks_valid_account_numbers[index]) == expected


@pytest.mark.parametrize(
    "index",
    [
        0,
        1,
        2,
    ],
)
def test_get_mask_account_invalid(
    masks_invalid_account_numbers: list[str],
    index: int,
) -> None:
    """Проверяет обработку некорректных счетов."""
    assert (
        get_mask_account(masks_invalid_account_numbers[index])
        == "Некорректный номер счета"
    )

