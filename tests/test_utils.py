import json
from pathlib import Path

from src.utils import load_transactions

"""Успешный запуск"""


def test_load_transactions_success(tmp_path: Path) -> None:
    file_path = tmp_path / "operations.json"

    transactions = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]

    file_path.write_text(
        json.dumps(transactions),
        encoding="utf-8",
    )

    result = load_transactions(str(file_path))

    assert result == transactions


"""JSON не содержит список"""


def test_load_transactions_not_list(tmp_path: Path) -> None:
    file_path = tmp_path / "operations.json"

    file_path.write_text(
        json.dumps({"id": 1, "amount": 100}),
        encoding="utf-8",
    )

    result = load_transactions(str(file_path))

    assert result == []


"""Такого файла не существует"""


def test_load_transactions_file_not_found(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.json"

    result = load_transactions(str(file_path))

    assert result == []


"""Некорректный JSON"""


def test_load_transactions_invalid_json(tmp_path: Path) -> None:
    file_path = tmp_path / "operations.json"

    file_path.write_text(
        "{ invalid json",
        encoding="utf-8",
    )

    result = load_transactions(str(file_path))

    assert result == []
