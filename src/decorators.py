import functools
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "app.log"

def log(filename=None, log_success=True):
    """Логирует выполнение функции и безопасно скрывает чувствительные данные."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)

                if log_success:
                    _write_log(f"{func.__name__} ok", filename)

                return result

            except Exception as e:
                error_type = type(e).__name__

                safe_args = tuple(
                    _mask_sensitive_value(arg) for arg in args
                )
                safe_kwargs = {
                    k: _mask_sensitive_value(v)
                    for k, v in kwargs.items()
                }

                message = (
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {safe_args}, {safe_kwargs}"
                )
                _write_log(message, filename)
                raise

        return wrapper

    return decorator


def _mask_sensitive_value(value):
    """Маскирует строки, похожие на номера карт и счетов."""

    if isinstance(value, str):
        clean_str = value.replace(" ", "")
        if clean_str.isdigit() and 12 <= len(clean_str) <= 20:
            return f"{clean_str[:4]}********{clean_str[-4:]}"

    return value


def _write_log(message, filename):
    """Записывает сообщение в файл или выводит его в консоль."""

    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
