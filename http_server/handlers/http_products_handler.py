from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import Product, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function
from database import list_products as sql_list_products, get_product as sql_get_products, \
    add_product as sql_add_product, update_product as sql_update_product, delete_product as sql_delete_product

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()


# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_products(payload=payload) executes.
@router.get("", response_model=HttpListResponse[Product])
def list_products(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                  _=Depends(check_authorization)):  # (payload=Depends(check_authorization)):
    """Fetch all products"""
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        products = sql_list_products(offset, limit, filter)
        return products  # JSON object
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching products: {str(e)}")


@router.get("/{id}", response_model=Product)
def get_product(id: int, _=Depends(check_authorization)):
    """Fetch one product by ID, authorized only"""
    try:
        product = sql_get_products(id)  # your SQL function that fetches a single center
        if not product:
            # No row returned → center not found
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Product with ID {product} not found")
        # Return just the object, status code 200 by default
        return product  # JSON object with status + data
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching products: {str(e)}")


@router.post("", response_model=int)
def create_product(product: Product, _=Depends(check_authorization)):
    """Create a new product (ID auto-generated)"""
    try:
        return sql_add_product(product)  # The new JSON object id
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching products: {str(e)}")


@router.put("", response_model=int)
def update_product(product: Product, _=Depends(check_authorization)):
    """Create a new product (ID auto-generated)"""
    try:
        return sql_update_product(product)  # The new JSON object id
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching products: {str(e)}")


@router.delete("/{id}")
def delete_product(id: int, _=Depends(check_authorization)):
    """Delete a product by ID"""
    try:
        if not sql_delete_product(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Product with ID {id} not found")
        return  # No content, 204 will be sent
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching products: {str(e)}")
