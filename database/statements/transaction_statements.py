# transaction_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import Transaction, HttpListResponse


def add_transaction(transaction: Transaction) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO transactions (supplier_id, date, product_id, type, quantity, price, tax, discount)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """,
                       (transaction.supplier_id, transaction.date, transaction.product_id, transaction.type,
                        transaction.quantity, transaction.price, transaction.tax, transaction.discount))
        conn.commit()
        return cursor.lastrowid


def update_transaction(transaction: Transaction) -> int:
    with db_lock:
        if transaction.id is None:
            raise ValueError("Transaction ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE transactions
                       SET supplier_id      = ?,
                           date       = ?,
                           product_id = ?,
                           type       = ?,
                           price      = ?,
                           quantity   = ?,
                           tax        = ?,
                           discount   = ?
                       WHERE id = ?
                       """, (
                           transaction.supplier, transaction.date, transaction.product_id,
                           transaction.type, transaction.price, transaction.quantity, transaction.tax, transaction.discount,
                           transaction.id
                       ))
        conn.commit()
        return cursor.rowcount


def delete_transaction(transaction_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_transaction(transaction_id: int) -> Transaction | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        row = cursor.fetchone()
        return Transaction(**dict(row)) if row else None


# --- Global filter expression for transactions ---
TRANSACTION_FILTER_EXPR: str = "(supplier_id || ' ' || product_id || ' ' || date || ' ' || type || ' ' || price || ' ' || quantity || ' ' || tax || ' ' || discount)"


def _list_transactions_by_type(offset: int, limit: int, filter: Optional[str] = None, tx_type: Optional[int] = None) -> \
HttpListResponse[Transaction]:
    """
    Internal helper to retrieve transactions with optional type (1=income, -1=outcome, None=all).
    """
    with db_lock:
        conn, cursor = get_connection()
        params: list = []
        query = "SELECT * FROM transactions"
        count_query = "SELECT COUNT(*) FROM transactions"

        # WHERE conditions
        where_clauses = []
        if tx_type is not None:
            where_clauses.append("type = ?")
            params.append(tx_type)

        if filter is not None:
            pattern = f"%{filter}%"
            where_clauses.append(f"{TRANSACTION_FILTER_EXPR} LIKE ?")
            params.append(pattern)

        if where_clauses:
            where_sql = " WHERE " + " AND ".join(where_clauses)
            query += where_sql
            count_query += where_sql

        # total count
        total = cursor.execute(count_query, params).fetchone()[0]

        # pagination
        if limit >= 0:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        transactions = [Transaction(**dict(r)) for r in rows]
        return HttpListResponse[Transaction](total=total, body=transactions)


def list_transactions(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Transaction]:
    """Retrieve all transactions."""
    return _list_transactions_by_type(offset, limit, filter=filter, tx_type=None)


def list_income_transactions(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Transaction]:
    """Retrieve all income transactions (type = 1)."""
    return _list_transactions_by_type(offset, limit, filter=filter, tx_type=1)


def list_outcome_transactions(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Transaction]:
    """Retrieve all outcome transactions (type = -1)."""
    return _list_transactions_by_type(offset, limit, filter=filter, tx_type=-1)
