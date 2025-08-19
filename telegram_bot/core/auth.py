import jwt
from core.config import POST_SERVICE_KEY
from datetime import datetime, timedelta, timezone


def create_jwt(sub:str = "bot",algorithm:str = "HS256"):
    return jwt.encode(
        {"sub": sub,
         "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
        },
        POST_SERVICE_KEY,
        algorithm
    )

print(create_jwt())
