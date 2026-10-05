import json
import os

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)
path = os.path.join(BASE_DIR, "data", "operations.json")


def load_transactions(path: str) -> list[dict]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []

        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []


data_list = load_transactions(path)
print(json.dumps(data_list, indent=4, ensure_ascii=False))
