import jwt
from backend.core.config import POST_SERVICE_KEY
from datetime import datetime, timedelta, timezone




def decode_jwt(token:str, algorithm: str = "HS256") -> dict[str,str]:
    """
    WARNING: 
        this function doesn't hold any of exceptions 
    """
    payload = jwt.decode(
        token,
        POST_SERVICE_KEY,
        [algorithm]
    )
    return payload



def create_jwt(sub:str = "website",algorithm:str = "HS256"):
    return jwt.encode(
        {"sub": sub,
         "exp": datetime.now(timezone.utc) + timedelta(hours = 1)
        },
        POST_SERVICE_KEY,
        algorithm
    )

print(create_jwt())
