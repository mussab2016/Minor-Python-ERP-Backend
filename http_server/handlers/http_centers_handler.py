from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import Center, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function
from database import list_centers as sql_list_centers, get_center as sql_get_center, add_center as sql_add_center, \
    update_center as sql_update_center, \
    delete_center as sql_delete_center

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()


# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_centers(payload=payload) executes.
@router.get("", response_model=HttpListResponse[Center])
def list_centers(page: Optional[str] = Query(None), filter: Optional[str] = Query(None), _=Depends(check_authorization)):
    """Fetch all center"""
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        centers = sql_list_centers(offset, limit, filter)
        return centers  # JSON object
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching centers: {str(e)}")


@router.get("/{id}", response_model=Center)
def get_center(id: int, _=Depends(check_authorization)):
    """Fetch one center by ID, authorized only"""
    try:
        center = sql_get_center(id)  # your SQL function that fetches a single center
        if not center:
            # No row returned → center not found
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Center with ID {id} not found")
        return center  # JSON object
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching centers: {str(e)}")


@router.post("", response_model=int)
def create_center(center: Center, _=Depends(check_authorization)):
    """Create a new center (ID auto-generated)"""
    try:
        return sql_add_center(center)  # the new center id
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching centers: {str(e)}")


@router.put("", response_model=int)
def update_center(center: Center, _=Depends(check_authorization)):
    """Create a new center (ID auto-generated)"""
    try:
        return sql_update_center(center)  # the new center id
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching centers: {str(e)}")


@router.delete("/{id}")
def delete_center(id: int, _=Depends(check_authorization)):
    """Delete a center by ID"""
    try:
        if not sql_delete_center(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Center with ID {id} not found")
        return
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching centers: {str(e)}")
