import secrets

from loguru import logger
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"


def create_access_token(
    username: str, user_id: int, expires_delta: timedelta = timedelta(minutes=30)
) -> str:
    """
    Function to create an access token.
    """
    expires = datetime.utcnow() + expires_delta
    to_encode = {"sub": username, "id": user_id, "exp": expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    """
    Function to decode a token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        logger.debug(f"payload: {payload}")
        username: str = payload.get("sub")
        logger.debug(f"username: {username}")
        return username
    except JWTError as e:
        if isinstance(e, jwt.ExpiredSignatureError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        elif isinstance(e, jwt.JWTClaimsError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate claims"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token"
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not decode token"
        )
