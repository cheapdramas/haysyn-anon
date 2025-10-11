from functools import wraps
from fastapi import HTTPException, status
import traceback

def fall_free():
    """
    Декоратор який не дасть декоратору бахнуть 500 без нашої волі
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                # уже оброблена помилка — не чіпаємо
                raise
            except Exception as e:
                tb = traceback.format_exc()
                print(f"[fall_free] Error in {func.__name__}: {e}\n{tb}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Technical issues"
                )
        return wrapper
    return decorator
