import pytest
from src.decorators import log


#ТЕСТЫ ДЛЯ ВЫВОДА В КОНСОЛЬ


def test_log_console_success(capsys):
    """Тест выполнения функции с выводом в консоль."""

    @log()
    def add(x, y):
        return x + y

    result = add(1, 2)

    assert result == 3
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_log_console_error(capsys):
    """Тест логирования ошибки при выводе в консоль."""

    @log()
    def divide(x, y):
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    expected_msg = "divide error: ZeroDivisionError. Inputs: (1, 0), {}"
    assert captured.out.strip() == expected_msg