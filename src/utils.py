import json
import os
from src.logs import get_logger

logger = get_logger("src.utils", "utils.log")


"""пришлось использовать чтобы код видел json файл"""
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
path = os.path.join(BASE_DIR, "data", "operations.json")

"""функция чтения файла"""


def load_transactions(path: str) -> list[dict]:
    logger.debug("Начало работы функции")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            logger.error("Файл пустой")
            return []
        logger.info("Все корректно")
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Файл не найден")
        return []
