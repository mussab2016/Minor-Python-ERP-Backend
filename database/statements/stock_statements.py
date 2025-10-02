# stock_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import Stock, HttpListResponse


def add_stock(stock: Stock) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO stocks (name, city, address, center_id)
                       VALUES (?, ?, ?, ?)
                       """, (stock.name, stock.city, stock.address, stock.center_id))
        conn.commit()
        return cursor.lastrowid


def update_stock(stock: Stock) -> int:
    with db_lock:
        if stock.id is None:
            raise ValueError("Stock ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE stocks
                       SET name      = ?,
                           city      = ?,
                           address   = ?,
                           center_id = ?
                       WHERE id = ?
                       """, (
                           stock.name, stock.city, stock.address, stock.center_id,
                           stock.id
                       ))
        conn.commit()
        return cursor.rowcount


def delete_stock(stock_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM stocks WHERE id = ?", (stock_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_stock(stock_id: int) -> Stock | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM stocks WHERE id = ?", (stock_id,))
        row = cursor.fetchone()
        return Stock(**dict(row)) if row else None


def list_stocks(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Stock]:
    """
    Retrieve all stocks with optional filtering.
    Returns a HttpListResponse[Stock] object.
    """
    with db_lock:
        conn, cursor = get_connection()
        filter_expr = "(name || ' ' || city || ' ' || address)"
        params: list = []
        query = "SELECT * FROM stocks"
        count_query = "SELECT COUNT(*) FROM stocks"

        if filter:
            query += f" WHERE {filter_expr} LIKE ?"
            count_query += f" WHERE {filter_expr} LIKE ?"
            params.append(f"%{filter}%")

        total = cursor.execute(count_query, params).fetchone()[0]

        if limit > 0:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        stocks = [Stock(**dict(r)) for r in rows]
        return HttpListResponse[Stock](total=total, body=stocks)
