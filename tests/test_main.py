from unittest.mock import patch

from src.main import main

TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2024-01-15T10:00:00Z",
        "description": "Перевод организации",
        "operationAmount": {
            "amount": "1000",
            "currency": {"name": "Рубль", "code": "RUB"},
        },
        "from": "Счет 123456789012",
        "to": "Счет 987654321098",
    },
    {
        "id": 2,
        "state": "CANCELED",
        "date": "2024-01-16T10:00:00Z",
        "description": "Оплата товаров",
        "operationAmount": {
            "amount": "50",
            "currency": {"name": "Доллар", "code": "USD"},
        },
        "from": "Visa 1234567890123456",
        "to": "Счет 987654321098",
    },
]


@patch("src.main.print_transactions")
@patch("src.main.filter_by_state")
@patch("src.main.load_transactions")
@patch("builtins.input")
def test_main_json_without_additional_filters(
    mock_input,
    mock_load,
    mock_filter,
    mock_print,
):
    mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]
    mock_load.return_value = TRANSACTIONS
    mock_filter.return_value = [TRANSACTIONS[0]]

    main()

    mock_load.assert_called_once_with("1")
    mock_filter.assert_called_once_with(TRANSACTIONS, "EXECUTED")
    mock_print.assert_called_once_with([TRANSACTIONS[0]])


@patch("src.main.print_transactions")
@patch("src.main.sort_by_date")
@patch("src.main.load_transactions")
@patch("builtins.input")
def test_main_sort_by_date(
    mock_input,
    mock_load,
    mock_sort,
    mock_print,
):
    mock_input.side_effect = [
        "1",
        "EXECUTED",
        "да",
        "по возрастанию",
        "нет",
        "нет",
    ]
    mock_load.return_value = TRANSACTIONS
    mock_sort.return_value = TRANSACTIONS

    with patch("src.main.filter_by_state", return_value=TRANSACTIONS):
        main()

    mock_sort.assert_called_once_with(TRANSACTIONS, reverse=False)
    mock_print.assert_called_once_with(TRANSACTIONS)


@patch("src.main.print_transactions")
@patch("src.main.process_bank_searching")
@patch("src.main.load_transactions")
@patch("builtins.input")
def test_main_search_by_word(
    mock_input,
    mock_load,
    mock_search,
    mock_print,
):
    mock_input.side_effect = [
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "да",
        "перевод",
    ]
    mock_load.return_value = TRANSACTIONS
    mock_search.return_value = [TRANSACTIONS[0]]

    with patch("src.main.filter_by_state", return_value=TRANSACTIONS):
        main()

    mock_search.assert_called_once_with(TRANSACTIONS, "перевод")
    mock_print.assert_called_once_with([TRANSACTIONS[0]])


@patch("src.main.print_transactions")
@patch("src.main.load_transactions")
@patch("builtins.input")
def test_main_rub_filter(
    mock_input,
    mock_load,
    mock_print,
):
    mock_input.side_effect = [
        "1",
        "EXECUTED",
        "нет",
        "да",
        "нет",
    ]
    mock_load.return_value = TRANSACTIONS

    with patch("src.main.filter_by_state", return_value=TRANSACTIONS):
        main()

    mock_print.assert_called_once_with([TRANSACTIONS[0]])


@patch("src.main.load_transactions", side_effect=OSError("Файл не найден"))
@patch("builtins.input", side_effect=["1", "EXECUTED"])
def test_main_file_loading_error(mock_input, mock_load, capsys):
    main()

    output = capsys.readouterr().out

    assert "Не удалось загрузить файл" in output


@patch("src.main.process_bank_searching", return_value=[])
@patch("src.main.load_transactions")
@patch("builtins.input")
def test_main_no_matching_transactions(
    mock_input,
    mock_load,
    mock_search,
    capsys,
):
    mock_input.side_effect = [
        "1",
        "EXECUTED",
        "нет",
        "нет",
        "да",
        "несуществующее слово",
    ]
    mock_load.return_value = TRANSACTIONS

    with patch("src.main.filter_by_state", return_value=TRANSACTIONS):
        main()

    output = capsys.readouterr().out

    assert "Не найдено ни одной транзакции" in output
