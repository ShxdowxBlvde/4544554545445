import functools


def log():
    """Декоратор, который автоматически логирует выполнение функции в консоль
    Безопасно скрывает номера карт и счетов при возникновении ошибок
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Успешное выполнение функции
                result = func(*args, **kwargs)
                print(f"{func.__name__} ok")
                return result

            except Exception as e:
                # Обработка ошибки
                error_type = type(e).__name__

                # Маскируем аргументы перед выводом в консоль для безопасности данных
                safe_args = tuple(_mask_sensitive_value(arg) for arg in args)
                safe_kwargs = {k: _mask_sensitive_value(v) for k, v in kwargs.items()}

                print(
                    f"{func.__name__} error: {error_type}. "
                    f"Inputs: {safe_args}, {safe_kwargs}"
                )
                # Пробрасываем ошибку дальше
                raise e

        return wrapper

    return decorator


def _mask_sensitive_value(value):
    """Вспомогательная функция для защиты персональных данных:
    Скрывает центральную часть строк, похожих на номера карт или счетов
    """
    if isinstance(value, str):
        clean_str = value.replace(" ", "")
        # Если строка состоит только из цифр и её длина от 12 до 20 символов
        if clean_str.isdigit() and 12 <= len(clean_str) <= 20:
            return f"{clean_str[:4]}********{clean_str[-4:]}"
    return value
