import jwt
from core.config import KEY, SECRET_SALT
from datetime import datetime, timedelta, timezone
from hashlib import sha256

def create_jwt(sub:str = "bot",algorithm:str = "HS256"):
    return jwt.encode(
        {"sub": sub,
         "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
        },
        KEY,
        algorithm
    )


def anonymize_user_id(telegram_user_id: str):
    return sha256(f"{telegram_user_id}{SECRET_SALT}".encode()).hexdigest()
