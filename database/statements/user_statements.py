# user_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import User, HttpListResponse


def add_user(user: User) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO users (name, username, password, rank)
                       VALUES (?, ?, ?, ?)
                       """, (user.name, user.username, user.password, user.rank))
        conn.commit()
        return cursor.lastrowid


def update_user(user: User) -> int:
    with db_lock:
        if user.id is None:
            raise ValueError("User ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE users
                       SET username     = ?,
                           password     = ?,
                           access_right = ?
                       WHERE id = ?
                       """, (
                           user.username, user.password, user.access_right,
                           user.id
                       ))
        conn.commit()
        return cursor.rowcount


def delete_user(user_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_user(user_id: int) -> User | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return User(**dict(row)) if row else None


USER_FILTER_EXPR: str = "(name || ' ' || rank)"


def list_users(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[User]:
    with db_lock:
        conn, cursor = get_connection()
        filter_expr = "(name || ' ' || rank)"
        params: list = []
        query = "SELECT * FROM users"
        count_query = "SELECT COUNT(*) FROM users"

        if filter:
            query += f" WHERE {filter_expr} LIKE ?"
            count_query += f" WHERE {filter_expr} LIKE ?"
            params.append(f"%{filter}%")

        total = cursor.execute(count_query, params).fetchone()[0]
        print(limit)
        if limit > 0:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        users = [User(**dict(r)) for r in rows]
        return HttpListResponse[User](total=total, body=users)


def get_user_by_username(username: str) -> User | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return User(**dict(row)) if row else None
