# center_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import Center, HttpListResponse


def add_center(center: Center) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO centers (name, city, address, phone, email)
                       VALUES (?, ?, ?, ?, ?)
                       """, (center.name, center.city, center.address, center.phone, center.email))
        conn.commit()
        return cursor.lastrowid


def update_center(center: Center) -> int:
    """
    Update an existing center in the database.
    Returns the number of rows affected.
    """
    with db_lock:
        if center.id is None:
            raise ValueError("Center ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE centers
                       SET name    = ?,
                           city    = ?,
                           address = ?,
                           phone   = ?,
                           email   = ?
                       WHERE id = ?
                       """, (center.name, center.city, center.address, center.phone, center.email, center.id))
        conn.commit()

        return cursor.rowcount  # number of rows updated


def delete_center(center_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM centers WHERE id = ?", (center_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_center(center_id: int) -> Center | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM centers WHERE id = ?", (center_id,))
        row = cursor.fetchone()
        return Center(**dict(
            row)) if row else None  # **dict(r) unpacks the row dictionary from SQLite into keyword arguments for the class constructor.


def list_centers(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Center]:
    """
    Retrieve all centers with optional filtering.
    """
    with db_lock:
        conn, cursor = get_connection()
        filter_expr = "(name || ' ' || city || ' ' || address || ' ' || phone || ' ' || email)"
        params: list = []
        query = "SELECT * FROM centers"
        count_query = "SELECT COUNT(*) FROM centers"

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
        centers = [Center(**dict(r)) for r in rows]
        return HttpListResponse[Center](total=total, body=centers)
