from typing import Any, Dict, List
import re
from src.decorators import log, LOG_FILE


@log(filename=str(LOG_FILE))
def filter_by_state(
    data: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'.

    Args:
        data: Список словарей для фильтрации.
        state: Значение статуса, по которому оставляем элементы.
            По умолчанию 'EXECUTED'.

    Returns:
        Новый список словарей, у которых ключ 'state' совпадает с заданным.
    """
    return [item for item in data if item.get("state") == state]


@log(filename=str(LOG_FILE))
def sort_by_date(
    data: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по ключу 'date'.

    Args:
        data: Список словарей для сортировки.
        reverse: Флаг направления сортировки. Если True, то сортирует
            по убыванию (от свежих к старым). По умолчанию True.

    Returns:
        Новый отсортированный список словарей.
    """
    # Используем пустую строку в качестве дефолта, чтобы избежать ошибок,
    # если ключ 'date' отсутствует в каком-либо словаре
    return sorted(data, key=lambda item: item.get("date") or "", reverse=reverse)


def process_bank_searching(data: list[dict], search: str) -> list[dict]:
    """
    фильтрует список банковских операций по строк поиска в описании
    """
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = []
    for operation in data:
        description = operation.get("description", "")

        if pattern.search(description):
            filtered_data.append(operation)

    return filtered_data


def process_bank_operations(
    data: list[dict],
    categories: list[str],
) -> dict[str, int]:
    category_counts = {category: 0 for category in categories}
    for operation in data:
        description = operation.get("description", "")
        if not description:
            continue

        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                category_counts[category] += 1

    return category_counts
