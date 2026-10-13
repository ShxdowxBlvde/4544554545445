
import json
from pathlib import Path
from datetime import datetime

from src.processing import (
    filter_by_state,
    sort_by_date,
    process_bank_searching,
)
from src.generators import filter_by_currency
from src.readers import read_csv_transactions, read_xlsx_transactions
from src.widget import mask_account_card


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_transactions(file_type: str) -> list[dict]:
    """Загружает транзакции из выбранного файла."""

    if file_type == "1":
        file_path = DATA_DIR / "operations.json"
        with file_path.open("r", encoding="utf-8") as file:
            transactions = json.load(file)

    elif file_type == "2":
        file_path = DATA_DIR / "transactions.csv"
        transactions = read_csv_transactions(str(file_path))

    elif file_type == "3":
        file_path = DATA_DIR / "transactions_excel.xlsx"
        transactions = read_xlsx_transactions(str(file_path))

    else:
        raise ValueError("Неизвестный тип файла")

    if not isinstance(transactions, list):
        raise ValueError("Файл должен содержать список транзакций")

    return [item for item in transactions if item]


def ask_yes_no(question: str) -> bool:
    """Запрашивает ответ Да/Нет."""

    while True:
        answer = input(f"\nПрограмма: {question} Да/Нет\n\nПользователь: ")
        answer = answer.strip().lower()

        if answer in ("да", "д", "yes", "y"):
            return True
        if answer in ("нет", "н", "no", "n"):
            return False

        print("\nПрограмма: введите Да или Нет.")


def get_currency_code(transaction: dict) -> str:
    """Возвращает код валюты для разных форматов транзакций."""

    operation_amount = transaction.get(
        "operationAmount",
        transaction.get("operation_amount"),
    )

    if isinstance(operation_amount, dict):
        currency = operation_amount.get("currency", {})
        if isinstance(currency, dict):
            code = currency.get("code")
            if code:
                return str(code).upper()

    code = transaction.get("currency_code", transaction.get("currency", ""))
    if isinstance(code, dict):
        return str(code.get("code", "")).upper()

    return str(code).upper()


def get_amount_and_currency(transaction: dict) -> tuple[str, str]:
    """Получает сумму и название валюты."""

    operation_amount = transaction.get(
        "operationAmount",
        transaction.get("operation_amount"),
    )

    if isinstance(operation_amount, dict):
        amount = operation_amount.get("amount", "")
        currency = operation_amount.get("currency", {})
        if isinstance(currency, dict):
            currency_name = currency.get("name", currency.get("code", ""))
        else:
            currency_name = str(currency)
        return str(amount), str(currency_name)

    amount = transaction.get("amount", "")
    currency = transaction.get(
        "currency_name",
        transaction.get("currency", transaction.get("currency_code", "")),
    )

    if isinstance(currency, dict):
        currency = currency.get("name", currency.get("code", ""))

    return str(amount), str(currency)


def format_date(date_value: object) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ."""

    if not date_value:
        return ""

    if isinstance(date_value, datetime):
        return date_value.strftime("%d.%m.%Y")

    date_string = str(date_value)

    for date_format in (
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            return datetime.strptime(
                date_string[:26] if "%f" in date_format else date_string,
                date_format,
            ).strftime("%d.%m.%Y")
        except ValueError:
            continue

    return date_string


def print_transactions(transactions: list[dict]) -> None:
    """Выводит список банковских операций."""

    if not transactions:
        print(
            "\nПрограмма: Не найдено ни одной транзакции, "
            "подходящей под ваши условия фильтрации"
        )
        return

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    print(
        f"\nПрограмма: \nВсего банковских операций в выборке: "
        f"{len(transactions)}\n"
    )

    for transaction in transactions:
        date = format_date(transaction.get("date", ""))
        description = transaction.get("description", "Без описания")

        from_info = transaction.get("from", "")
        to_info = transaction.get("to", "")

        if from_info and to_info:
            payment_line = (
                f"{mask_account_card(str(from_info))} -> "
                f"{mask_account_card(str(to_info))}"
            )
        elif to_info:
            payment_line = mask_account_card(str(to_info))
        else:
            payment_line = ""

        amount, currency = get_amount_and_currency(transaction)

        print(f"{date} {description}")
        if payment_line:
            print(payment_line)
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """Основная логика программы для работы с банковскими транзакциями."""

    print(
        "Программа: Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("\nПользователь: ").strip()

        if choice in ("1", "2", "3"):
            break

        print("\nПрограмма: выберите 1, 2 или 3.")

    file_names = {
        "1": "JSON",
        "2": "CSV",
        "3": "XLSX",
    }

    print(f"\nПрограмма: Для обработки выбран {file_names[choice]}-файл.")

    try:
        transactions = load_transactions(choice)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"\nПрограмма: Не удалось загрузить файл: {error}")
        return

    valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        print(
            "\nПрограмма: Введите статус, по которому необходимо "
            "выполнить фильтрацию."
        )
        print(
            "Доступные для фильтровки статусы: "
            "EXECUTED, CANCELED, PENDING"
        )

        status = input("\nПользователь: ").strip().upper()

        if status in valid_statuses:
            transactions = filter_by_state(transactions, status)
            print(
                f'\nПрограмма: Операции отфильтрованы по статусу "{status}"'
            )
            break

        print(
            f'\nПрограмма: Статус операции "{status}" недоступен.'
        )

    if ask_yes_no("Отсортировать операции по дате?"):
        while True:
            order = input(
                "\nПрограмма: Отсортировать по возрастанию "
                "или по убыванию?\n\nПользователь: "
            ).strip().lower()

            if order in ("по возрастанию", "возрастанию"):
                transactions = sort_by_date(transactions, reverse=False)
                break

            if order in ("по убыванию", "убыванию"):
                transactions = sort_by_date(transactions, reverse=True)
                break

            print(
                "\nПрограмма: введите «по возрастанию» "
                "или «по убыванию»."
            )

    if ask_yes_no("Выводить только рублевые транзакции?"):
        transactions = [
            transaction
            for transaction in transactions
            if get_currency_code(transaction) == "RUB"
        ]

    if ask_yes_no(
        "Отфильтровать список транзакций по определенному слову "
        "в описании?"
    ):
        search_word = input(
            "\nПрограмма: Введите слово для поиска.\n\nПользователь: "
        ).strip()

        transactions = process_bank_searching(
            transactions,
            search_word,
        )

    print_transactions(transactions)


if __name__ == "__main__":
    main()
