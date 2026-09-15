def get_mask_card_number(card_number: str) -> str:
    """маскирует номер банковской карточки.
    формат маскировки: XXXX XX** **** XXXX
    пример: 7000792289606361 -> 7000 79** **** 6361
    """
    # Удаляем пробелы, если они были во входной строке
    cleaned = card_number.replace(" ", "")

    if len(cleaned) != 16 or not cleaned.isdigit():
        return "Некорректный номер карты"

    first_block = cleaned[:4]
    second_block = f"{cleaned[4:6]}**"
    third_block = "****"
    fourth_block = cleaned[12:]

    return f"{first_block} {second_block} {third_block} {fourth_block}"


def get_mask_account(account_number: str) -> str:
    """маскирует номер банковского счета.
    формат маскировки: **XXXX (видны только последние 4 цифры)
    пример: 73654108430135874305 -> **4305
    """
    if len(account_number) < 4 or not account_number.isdigit():
        return "Некорректный номер счета"

    return f"**{account_number[-4:]}"
