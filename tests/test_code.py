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


#MASKS


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "7000 79** **** 6361"),
        (1, "1234 56** **** 5678"),
        (2, "7000 79** **** 6361"),
    ],
)
def test_get_mask_card_number_valid(
    masks_valid_card_numbers,index,expected,
):
    """Проверяет корректное маскирование номеров карт."""
    assert get_mask_card_number(masks_valid_card_numbers[index]) == expected


@pytest.mark.parametrize(
    "index",
    [0,1,2,3,4,],
)
def test_get_mask_card_number_invalid(masks_invalid_card_numbers,index,):

    """Проверяет обработку некорректных номеров карт."""
    assert (get_mask_card_number(masks_invalid_card_numbers[index]) == "Некорректный номер карты")


@pytest.mark.parametrize(
    "index, expected",
    [(0, "**4305"),(1, "**5678"),(2, "**1234"),],
)
def test_get_mask_account_valid(masks_valid_account_numbers,index,expected,):
    """Проверяет корректное маскирование счетов."""
    assert get_mask_account(masks_valid_account_numbers[index]) == expected


@pytest.mark.parametrize(
    "index",
    [0,1,2,],)
def test_get_mask_account_invalid(masks_invalid_account_numbers,index,):
    """Проверяет обработку некорректных счетов."""
    assert (get_mask_account(masks_invalid_account_numbers[index]) == "Некорректный номер счета")



# WIDGET


@pytest.mark.parametrize(
    "index",
    [ 0,1,2,],
)
def test_mask_account_card_valid(widget_valid_card_numbers,index,):
    """Проверяет маскирование карт и счетов."""
    input_data, expected = widget_valid_card_numbers[index]

    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "index",
    [0,1,],
)
def test_mask_account_card_invalid(widget_invalid_card_numbers,index,):
    """Проверяет обработку некорректных данных."""
    input_data, expected = widget_invalid_card_numbers[index]

    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-01T00:00:00.000", "01.12.2023"),
        ("2025-01-05", "05.01.2025"),],)
def test_get_date_valid(date_string, expected):
    """Проверяет преобразование дат."""
    assert get_date(date_string) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("11-03-2024", "03.20.11"),
        ("not-a-date", "a.-t.not"),
        ("", ".."),],)

def test_get_date_unusual(date_string, expected):
    """Проверяет работу функции с нестандартными строками."""
    assert get_date(date_string) == expected


def test_get_date_none():
    """Проверяет ошибку при передаче None."""
    with pytest.raises(TypeError):
        get_date(None)


def test_mask_account_card_empty_string():
    """Проверяет ошибку при передаче пустой строки."""
    with pytest.raises(IndexError):
        mask_account_card("")


def test_mask_account_card_none():
    """Проверяет ошибку при передаче None."""
    with pytest.raises(AttributeError):
        mask_account_card(None)



# PROCESSING


@pytest.mark.parametrize("state, expected_ids",
    [
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),],
                         )

def test_filter_by_state(processing_transactions,state,expected_ids,):

    """Проверяет фильтрацию транзакций по статусу."""
    result = filter_by_state(processing_transactions,state,)

    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_default(processing_transactions):
    """Проверяет статус EXECUTED по умолчанию."""
    result = filter_by_state(processing_transactions)

    assert [item["id"] for item in result] == [1, 3]


def test_filter_by_state_empty(processing_empty_transactions):
    """Проверяет фильтрацию пустого списка."""
    assert filter_by_state(processing_empty_transactions) == []


@pytest.mark.parametrize(
    "reverse, expected_ids",
    [(True, [4, 2, 1, 3]),(False, [3, 1, 2, 4]),],
)
def test_sort_by_date(processing_transactions,reverse,expected_ids,):
    """Проверяет сортировку по датам."""
    result = sort_by_date(processing_transactions,reverse=reverse,)

    assert [item["id"] for item in result] == expected_ids


def test_sort_by_date_default(processing_transactions):
    """Проверяет сортировку по убыванию по умолчанию."""
    result = sort_by_date(processing_transactions)

    assert [item["id"] for item in result] == [4, 2, 1, 3]


def test_sort_by_date_empty(processing_empty_transactions):
    """Проверяет сортировку пустого списка."""
    assert sort_by_date(processing_empty_transactions) == []


def test_sort_by_date_without_date():
    """Проверяет обработку отсутствующего ключа date."""
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01"},
    ]

    result = sort_by_date(data)

    assert result[0]["id"] == 2
    assert result[1]["id"] == 1
