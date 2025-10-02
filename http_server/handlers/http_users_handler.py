# http_user_handler.py
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import User, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function
from database import list_users as sql_list_users, get_user as sql_get_user, add_user as sql_add_user, \
    update_user as sql_update_user, \
    delete_user as sql_delete_user

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_users(payload=payload) executes.
@router.get("", response_model=HttpListResponse[User])
def list_users(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),_=Depends(check_authorization)):
    offset: int = 1
    limit: int  = -1
    try:
        page, limit = map(int, page.split("-"))
        offset = page * limit
    except Exception:
        None
    try:
        return sql_list_users(offset, limit, filter) # make_list_response(users)
    except Exception as e:
        logger.exception("Error fetching users")
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching users: {str(e)}")


@router.get("/{id}", response_model=User)
def get_user(id: int, _=Depends(check_authorization)):
    try:
        user = sql_get_user(id)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching user: {str(e)}")


@router.post("", response_model=int)
def create_user(user: User, _=Depends(check_authorization)):
    try:
        return sql_add_user(user)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding user: {str(e)}")


@router.put("", response_model=int)
def update_user(user: User, _=Depends(check_authorization)):
    try:
        return sql_update_user(user)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding user: {str(e)}")


@router.delete("/{id}")
def delete_user(id: int, _=Depends(check_authorization)):
    try:
        if not sql_delete_user(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
        return
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting user: {str(e)}")
