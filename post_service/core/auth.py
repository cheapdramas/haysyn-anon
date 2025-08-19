from typing import Awaitable, Callable
from fastapi import (
    HTTPException, status, 
    Request, Security
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import POST_SERVICE_KEY

from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import jwt 
import snowflake
import functools


id_generator = snowflake.SnowflakeGenerator(1)

subs = ["bot", "website"]

def decode_jwt(token:str, algorithm: str = "HS256") -> dict[str,str]:
    """WARNING: 
        this function doesn't hold any of exceptions 
    """
    payload = jwt.decode(
        token,
        POST_SERVICE_KEY,
        [algorithm]
    )
    return payload

def verify_token(token: str, sub:str = "") -> dict:
    try:
        payload = decode_jwt(token)
        if sub == "":
            return payload
        if payload["sub"] != sub:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Bad token")

    except ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Token expired")
    except InvalidSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Bad token")
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= "Bad token")


auth_scheme = HTTPBearer()
def verify_token_depends(sub: str) -> Callable[[HTTPAuthorizationCredentials], Awaitable[str]]:
    
    async def check_token(auth_creds: HTTPAuthorizationCredentials = Security(auth_scheme)) -> str:
        token = auth_creds.credentials
        verify_token(token, sub)
        return token

    return check_token

