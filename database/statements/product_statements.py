# product_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import Product, HttpListResponse


def add_product(product: Product) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO products (name, description, stock_id, quantity, expiration_date, purchase_price, sale_price)
                       VALUES (?, ?, ?, ?, ?, ?, ?)
                       """, (product.name, product.description, product.stock_id, product.quantity, product.expiration_date,
                             product.purchase_price, product.sale_price))
        conn.commit()
        return cursor.lastrowid


def update_product(product: Product) -> int:
    with db_lock:
        if product.id is None:
            raise ValueError("Product ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE products
                       SET name            = ?,
                           description     = ?,
                           stock_id        = ?,
                           quantity        = ?,
                           expiration_date = ?,
                           purchase_price  = ?,
                           sale_price      = ?
                       WHERE id = ?
                       """, (
                           product.name, product.description, product.stock_id, product.quantity,
                           product.expiration_date, product.purchase_price, product.sale_price,
                           product.id
                       ))
        conn.commit()
        return cursor.rowcount


def delete_product(product_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_product(product_id: int) -> Product | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        return Product(**dict(row)) if row else None


def list_products(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Product]:
    """
    Retrieve all products.
    Returns a HttpListResponse[Product] object.
    """
    with db_lock:
        conn, cursor = get_connection()
        filter_expr = "(name || ' ' || description )"
        params: list = []
        query = "SELECT * FROM products"
        count_query = "SELECT COUNT(*) FROM products"

        if filter:
            query += f" WHERE {filter_expr} LIKE ?"
            count_query += f" WHERE {filter_expr} LIKE ?"
            params.append(f"%{filter}%")

        total = cursor.execute(count_query, params).fetchone()[0]

        if limit >= 0:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        products = [Product(**dict(r)) for r in rows]
        return HttpListResponse[Product](total=total, body=products)
