from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(info_string: str) -> str:
    """
    Принимает строку с типом и номером карты/счета.
    Возвращает строку с замаскированным номером.
    """
    # Разделяем строку по пробелам на отдельные элементы
    parts = info_string.split()

    # Все элементы, кроме последнего
    name_parts = parts[:-1]

    # Последний элемент — это всегда номер
    number_part = parts[-1]

    # Собираем название обратно в одну строку через пробел
    type_name = " ".join(name_parts)

    # Проверяем, что именно перед нами, и применяем нужную маску
    if type_name.lower().startswith("счет"):
        masked_number = get_mask_account(number_part)
    else:
        masked_number = get_mask_card_number(number_part)

    # Возвращаем название и замаскированный номер вместе
    return f"{type_name} {masked_number}"

