import functools
import sys


def log(filename=None):
    """Декоратор, который логирует выполнение функции в консоль или файл."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Выполняем декорируемую функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успешном выполнении
                message = f"{func.__name__} ok"

                _write_log(message, filename)
                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_type = type(e).__name__
                message = (
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {args}, {kwargs}"
                )

                _write_log(message, filename)
                # Пробрасываем ошибку дальше, чтобы не нарушать логику программы
                raise e

        return wrapper

    return decorator


def _write_log(message, filename):
    """Вспомогательная функция для записи лога в файл или консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
