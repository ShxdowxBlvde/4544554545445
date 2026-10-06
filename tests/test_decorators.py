import pytest

from src.decorators import log

# ТЕСТЫ ДЛЯ ВЫВОДА В КОНСОЛЬ (filename=None)


def test_log_console_success(capsys):
    """Тест успешного выполнения функции с выводом в консоль."""

    @log()
    def sample_success(x, y):
        return x + y

    result = sample_success(10, 20)

    assert result == 30
    captured = capsys.readouterr()
    assert captured.out.strip() == "sample_success ok"


def test_log_console_error(capsys):
    """Тест логирования ошибки при выводе в консоль."""

    @log()
    def sample_fail():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        sample_fail()

    captured = capsys.readouterr()
    assert captured.out.strip() == "sample_fail error: ValueError. Inputs: (), {}"


# ТЕСТЫ ДЛЯ ЗАПИСИ В ФАЙЛ (filename задан)


def test_log_file_success(tmp_path):
    """Тест успешного выполнения с записью в файл."""
    # Используем tmp_path от pytest, чтобы автоматически создать безопасный путь к файлу
    log_file = tmp_path / "success.log"

    @log(filename=str(log_file))
    def sample_file_func():
        return True

    sample_file_func()

    # Проверяем, что файл создался и содержит правильную запись
    assert log_file.exists()
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "sample_file_func ok"


def test_log_file_error(tmp_path):
    """Тест логирования ошибки с записью в файл."""
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def sample_file_fail(a, b=5):
        raise TypeError("File error")

    with pytest.raises(TypeError):
        sample_file_fail("hello", b=10)

    # Проверяем запись ошибки в файле
    assert log_file.exists()
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_msg = "sample_file_fail error: TypeError. Inputs: ('hello',), {'b': 10}"
    assert content == expected_msg


# ТЕСТЫ БЕЗОПАСНОСТИ (МАСКИРОВАНИЕ ДАННЫХ)


def test_log_masks_sensitive_data_on_error(capsys):
    """Проверяем, что декоратор скрывает номера карт/счетов при ошибках в консоли."""

    @log()
    def process_card(card_number):
        raise RuntimeError("Fail")

    with pytest.raises(RuntimeError):
        process_card("1234567812345678")  # Длина 16 цифр (номер карты)

    captured = capsys.readouterr()
    log_output = captured.out.strip()

    # Полный номер карты не должен попасть в консоль
    assert "1234567812345678" not in log_output
    # Вместо него должна быть маска
    assert "1234********5678" in log_output


# ТЕСТ СОХРАНЕНИЯ МЕТАДАННЫХ (functools.wraps)


def test_log_preserves_metadata():
    """Проверяем, что functools.wraps корректно сохраняет имя и docstring функции."""

    @log()
    def original_function():
        """Это важная документация функции."""
        return None

    assert original_function.__name__ == "original_function"
    assert original_function.__doc__ == "Это важная документация функции."
