from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import Supplier, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function
from database import list_suppliers as sql_list_suppliers, list_consumers as sql_list_customers, \
    list_providers as sql_list_providers, get_supplier as sql_get_supplier, \
    add_supplier as sql_add_supplier, update_supplier as sql_update_supplier, delete_supplier as sql_delete_supplier

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()


# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_suppliers(payload=payload) executes.
@router.get("", response_model=HttpListResponse[Supplier])
def list_suppliers(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                   _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass  # do nothing if parsing fails
    try:
        return sql_list_suppliers(offset, limit, filter)  # JSON object
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching suppliers: {str(e)}")


@router.get("/consumers", response_model=HttpListResponse[Supplier])
def list_customers(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                   _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        return sql_list_customers(offset, limit, filter)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching suppliers: {str(e)}")


@router.get("/providers", response_model=HttpListResponse[Supplier])
def list_providers(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                   _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        return sql_list_providers(offset, limit, filter)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching suppliers: {str(e)}")


@router.get("/{id}", response_model=Supplier)
def get_supplier(id: int, _=Depends(check_authorization)):
    try:
        supplier = sql_get_supplier(id)
        if not supplier:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Supplier with ID {id} not found")
        return supplier
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching supplier: {str(e)}")


@router.post("", response_model=int)
def create_supplier(supplier: Supplier, _=Depends(check_authorization)):
    try:
        return sql_add_supplier(supplier)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding supplier: {str(e)}")


@router.put("", response_model=int)
def update_supplier(supplier: Supplier, _=Depends(check_authorization)):
    try:
        return sql_update_supplier(supplier)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding supplier: {str(e)}")


@router.delete("/{id}")
def delete_supplier(id: int, _=Depends(check_authorization)):
    try:
        if not sql_delete_supplier(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Supplier with ID {id} not found")
        return
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting supplier: {str(e)}")
