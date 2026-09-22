from typing import Generator, List, Dict, Any

def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Generator[Dict[str, Any], None, None]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор
    """
    for transaction in transactions:
        # Проверяем наличие вложенных ключей, чтобы избежать ошибок KeyError
        try:
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction
        except KeyError:
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """
    Возвращает description каждой транзакции по очереди
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX в заданном диапазоне
    """
    for number in range(start, end + 1):
        # Дополняем число нулями слева до 16 знаков
        str_number = f"{number:016d}"
        # Форматируем строку, разделяя по 4 знака пробелами
        formatted_number = f"{str_number[:4]} {str_number[4:8]} {str_number[8:12]} {str_number[12:]}"
        yield formatted_number

