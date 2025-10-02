from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import Stock, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function

from database import list_stocks as sql_list_stocks, get_stock as sql_get_stock, add_stock as sql_add_stock, \
    update_stock as sql_update_stock, \
    delete_stock as sql_delete_stock

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()


# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_stocks(payload=payload) executes.
@router.get("", response_model=HttpListResponse[Stock])
def list_stocks(page: Optional[str] = Query(None), filter: Optional[str] = Query(None), _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        stocks = sql_list_stocks(offset, limit, filter)
        return stocks  # JSON object
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching stocks: {str(e)}")


@router.get("/{id}", response_model=Stock)
def get_stock(id: int, _=Depends(check_authorization)):
    try:
        stock = sql_get_stock(id)
        if not stock:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Stock with ID {id} not found")
        return stock
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching stock: {str(e)}")


@router.post("", response_model=int)
def create_stock(stock: Stock, _=Depends(check_authorization)):
    try:
        return sql_add_stock(stock)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding stock: {str(e)}")


@router.put("", response_model=int)
def update_stock(stock: Stock, _=Depends(check_authorization)):
    try:
        return sql_update_stock(stock)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding stock: {str(e)}")


@router.delete("/{id}")
def delete_stock(id: int, _=Depends(check_authorization)):
    try:
        if not sql_delete_stock(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Stock with ID {id} not found")
        return
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting stock: {str(e)}")
