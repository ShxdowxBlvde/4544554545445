from src.decorators import log
from src.logs import get_logger

logger = get_logger("src.masks", "masks.log")


@log()
def get_mask_card_number(card_number: str) -> str:
    logger.debug("Начало работы маскировки карты")
    """маскирует номер банковской карточки.
    формат маскировки: XXXX XX** **** XXXX
    пример: 7000792289606361 -> 7000 79** **** 6361
    """
    # Удаляем пробелы, если они были во входной строке
    cleaned = card_number.replace(" ", "")

    if len(cleaned) != 16 or not cleaned.isdigit():
        logger.error("Передан некорректный номер карты")
        return "Некорректный номер карты"

    first_block = cleaned[:4]
    second_block = f"{cleaned[4:6]}**"
    third_block = "****"
    fourth_block = cleaned[12:]
    logger.info("Вывод замаскированного номера карты")
    return f"{first_block} {second_block} {third_block} {fourth_block}"


@log()
def get_mask_account(account_number: str) -> str:
    logger.debug("Начало работы маскировки номера счета")
    """маскирует номер банковского счета.
    формат маскировки: **XXXX (видны только последние 4 цифры)
    пример: 73654108430135874305 -> **4305
    """
    if len(account_number) < 4 or not account_number.isdigit():
        logger.error("Введен некорректный номер счета")
        return "Некорректный номер счета"

    logger.info("Вывод замаскированного номера счета")
    return f"**{account_number[-4:]}"
