from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.params import Query
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from entities import Transaction, HttpListResponse
from http_server.authorization import check_authorization  # <-- your JWT verification function
from database import list_transactions as sql_list_transactions, \
    list_income_transactions as sql_list_incomes_transactions, \
    list_outcome_transactions as sql_list_outcomes_transactions, get_transaction as sql_get_transaction, \
    add_transaction as sql_add_transaction, update_transaction as sql_update_transaction, \
    delete_transaction as sql_delete_transaction

# -----------------------------
# Router definition
# -----------------------------
router = APIRouter()


# FastAPI will call the Depends and Verify the JWT. Then Raise an HTTP 401 if invalid. Return the decoded token payload if valid. FastAPI assigns the returned value to payload. Then the route list_users(payload=payload) executes.
@router.get("", response_model=HttpListResponse[Transaction])
def list_transactions(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                      _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        return sql_list_transactions(offset, limit, filter)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching transactions: {str(e)}")


@router.get("/incomes", response_model=HttpListResponse[Transaction])
def list_incomes_transactions(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                              _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass  # do nothing if parsing fails
    try:
        return sql_list_incomes_transactions(offset, limit, filter)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching transactions: {str(e)}")


@router.get("/outcomes", response_model=HttpListResponse[Transaction])
def list_outcomes_transactions(page: Optional[str] = Query(None), filter: Optional[str] = Query(None),
                               _=Depends(check_authorization)):
    offset: int = 1
    limit: int = -1
    try:
        page_num, limit = map(int, page.split("-"))
        offset = page_num * limit
    except Exception:
        pass
    try:
        return sql_list_outcomes_transactions(offset, limit, filter)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching transactions: {str(e)}")


@router.get("/{id}", response_model=Transaction)
def get_transaction(id: int, _=Depends(check_authorization)):
    try:
        transaction = sql_get_transaction(id)
        if not transaction:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f"Transaction with ID {id} not found")
        return transaction
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching transaction: {str(e)}")


@router.post("", response_model=int)
def create_transaction(transaction: Transaction, _=Depends(check_authorization)):
    try:
        return sql_add_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding transaction: {str(e)}")


@router.put("", response_model=int)
def update_transaction(transaction: Transaction, _=Depends(check_authorization)):
    try:
        return sql_update_transaction(transaction)
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error adding transaction: {str(e)}")


@router.delete("/{id}")
def delete_transaction(id: int, _=Depends(check_authorization)):
    try:
        if not sql_delete_transaction(id):
            raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                                detail=f"Transaction with ID {id} not found")
        return
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting transaction: {str(e)}")
