from typing import Any, Dict, List


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
