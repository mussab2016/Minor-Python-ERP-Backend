from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_user_by_username, verify_password  # fetch user from DB
from http_server.authorization import create_token, \
    check_authorization  # JWT creation function and JWT verification function

router = APIRouter()


class loginInfo(BaseModel):
    username: str
    password: str


@router.post("")
def login(data: loginInfo):
    user = get_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_token({"user_id": user.id, "username": user.username})
    return {"token": token}


@router.get("")  # /verify-token
def verify_token(_=Depends(check_authorization)):
    """
    Verify if the JWT token provided in the Authorization header is valid.
    Returns HTTP 200 if valid.
    Raises HTTP 401 if invalid or expired.
    """
    # If check_authorization succeeds, payload is valid
    return
