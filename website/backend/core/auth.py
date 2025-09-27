import jwt
import snowflake
from backend.core.config import KEY
from datetime import datetime, timedelta, timezone

from typing import Awaitable, Callable

from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError


id_generator = snowflake.SnowflakeGenerator(1)

subs = ["bot"]

def decode_jwt(token:str, algorithm: str = "HS256") -> dict[str,str]:
    """
    WARNING: 
        this function doesn't hold any of exceptions 
    """
    payload = jwt.decode(
        token,
        KEY,
        [algorithm]
    )
    return payload


def create_jwt(sub:str = "website",algorithm:str = "HS256"):
    return jwt.encode(
        {"sub": sub,
         "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
        },
        KEY,
        algorithm
    )


def verify_token(token: str, sub:str = "") -> dict:
    try:
        payload = decode_jwt(token)
        if sub == "":
            return payload
        if payload["sub"] != sub:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Bad token")
    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Token expired")
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Bad token")




auth_scheme = HTTPBearer()
def verify_token_depends(sub: str) -> Callable[[HTTPAuthorizationCredentials], Awaitable[str]]:
    
    async def check_token(auth_creds: HTTPAuthorizationCredentials = Security(auth_scheme)) -> str:
        token = auth_creds.credentials
        verify_token(token, sub)
        return token

    return check_token

