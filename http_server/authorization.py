# Authorization
from fastapi import Depends, HTTPException, Header, status
# ↑ FastAPI helpers:
#    - Depends: used later if you wire the check as a dependency in routes
#    - HTTPException: raise this to return an HTTP error response
#    - Header: used to extract an HTTP header value (Authorization)
#    - status: contains numeric HTTP status constants (e.g. status.HTTP_401_UNAUTHORIZED)
import jwt
# ↑ PyJWT library. Provides jwt.encode / jwt.decode.

from datetime import datetime, timedelta
# ↑ datetime utilities used to set token expiration time

SECRET_KEY = "mysecret"
# ↑ Secret key used to sign tokens. **DO NOT** hardcode in production — use an environment variable.

ALGORITHM = "HS256"
# ↑ The signing algorithm. HS256 means HMAC + SHA256 (symmetric key).

def create_token(data: dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """
    Generate a JWT token with given data and expiration.
    """
    to_encode = data.copy()
    # ↑ copy the payload dict so the caller's dict isn't modified
    expire = datetime.utcnow() + expires_delta
    # ↑ compute an expiration datetime (UTC). Default 24 hours from now
    to_encode.update({"exp": expire})
    # ↑ add the 'exp' claim to the payload. PyJWT will convert a datetime to a numeric timestamp
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # ↑ sign and encode the JWT. Returns a compact JWT string
    return f"Bearer {token}"
    # ↑ return with the "Bearer " prefix so it can be placed directly in the Authorization header


def check_authorization(authorization: str = Header(...)): # similarly as (auth: str = Header(..., alias="Authorization")):
    """
    Dependency to check Authorization header and verify JWT.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )
    # ↑ If header does not begin with "Bearer ", we reject with 401 Unauthorized.

    token = authorization.split(" ")[1]
    # ↑ split header "Bearer <token>" and extract the actual token string

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # ↑ decode and verify the token signature & claims (including exp).
        #   If valid, `payload` is the original dict we encoded (with any claims).

        return payload  # you can return user info from token
        # ↑ When used as a FastAPI dependency, the returned value (payload) is injected into routes.

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    # ↑ Handle common JWT errors and turn them into HTTP 401 responses.
