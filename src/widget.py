from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime

def mask_account_card(info_string: str) -> str:
    """Принимает строку с типом и номером карты/счета.

    Возвращает строку с замаскированным номером.
    """
    # Сохраняем падение с AttributeError при None
    if info_string is None:
        raise AttributeError("'NoneType' object has no attribute 'split'")

    # Разделяем по пробелам
    parts = info_string.split()

    # Сохраняем падение с IndexError при пустой строке
    if not parts:
        raise IndexError("list index out of range")

    # Проверяем, есть ли вообще цифры в последнем элементе
    if parts[-1].isdigit():
        number_part = parts[-1]
        type_name = " ".join(parts[:-1])
    else:
        # ЕСЛИ ЦИФР НЕТ Вся переданная строка целиком становится названием
        # для number_part передаем пустую строку или заглушку
        type_name = info_string
        return f"{type_name} Некорректный номер карты"

    # Проверяем тип (Счет или Карта) и применяем нужную маску
    if type_name.lower().startswith("счет"):
        masked_number = get_mask_account(number_part)
    else:
        masked_number = get_mask_card_number(number_part)

    return f"{type_name} {masked_number}"


def get_date(date_string: str) -> str:
    """Возвращает дату в формате ДД.ММ.ГГГГ."""

    date = datetime.fromisoformat(date_string)
    return date.strftime("%d.%m.%Y")
