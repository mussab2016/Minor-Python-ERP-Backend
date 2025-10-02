# supplier_statements.py
from typing import Optional

from .. import get_connection, db_lock
from entities import Supplier, HttpListResponse


def add_supplier(supplier: Supplier) -> int:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("""
                       INSERT INTO suppliers (firstname, lastname, type, contract_date)
                       VALUES (?, ?, ?, ?)
                       """, (supplier.firstname, supplier.lastname, supplier.type, supplier.contract_date))
        conn.commit()
        return cursor.lastrowid


def update_supplier(supplier: Supplier) -> int:
    with db_lock:
        if supplier.id is None:
            raise ValueError("Supplier ID must be provided for update")

        conn, cursor = get_connection()
        cursor.execute("""
                       UPDATE suppliers
                       SET firstname     = ?,
                           lastname      = ?,
                           type          = ?,
                           contract_date = ?
                       WHERE id = ?
                       """, (
                           supplier.firstname, supplier.lastname, supplier.type, supplier.contract_date,
                           supplier.id
                       ))
        conn.commit()
        return cursor.rowcount


def delete_supplier(supplier_id: int) -> bool:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was deleted. cursor.rowcount gives the number of affected rows


def get_supplier(supplier_id: int) -> Supplier | None:
    with db_lock:
        conn, cursor = get_connection()
        cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        row = cursor.fetchone()
        return Supplier(**dict(row)) if row else None


FILTER_EXPR: str = "(firstname || ' ' || lastname || ' ' || type)"


def _list_suppliers_by_type(offset: int, limit: int, filter: Optional[str] = None, type: Optional[int] = None) -> HttpListResponse[Supplier]:
    """
        Internal helper to retrieve suppliers with optional type (provider, consumer, None=all).
        """
    with db_lock:
        conn, cursor = get_connection()
        params: list = []
        query = "SELECT * FROM suppliers"
        count_query = "SELECT COUNT(*) FROM suppliers"

        # WHERE conditions
        where_clauses = []
        if type is not None:
            where_clauses.append("type IN (?,?)")
            params.append(type).append("both")

        if filter is not None:
            pattern = f"%{filter}%"
            where_clauses.append(f"{FILTER_EXPR} LIKE ?")
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
        suppliers = [Supplier(**dict(r)) for r in rows]
        return HttpListResponse[Supplier](total=total, body=suppliers)

def list_suppliers(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Supplier]:
    return _list_suppliers_by_type(offset, limit, filter=filter, type=None)
    # conn, cursor = get_connection()
    #
    # if filter is not None:
    #     pattern = f"%{filter}%"
    #     total = cursor.execute(
    #         f"SELECT COUNT(*) FROM suppliers WHERE {filter_expr} LIKE ?",
    #         (pattern,)
    #     ).fetchone()[0]
    #
    #     if limit == -1:
    #         cursor.execute(f"SELECT * FROM suppliers WHERE {filter_expr} LIKE ?", (pattern,))
    #     else:
    #         cursor.execute(
    #             f"SELECT * FROM suppliers WHERE {filter_expr} LIKE ? LIMIT ? OFFSET ?",
    #             (pattern, limit, offset)
    #         )
    # else:
    #     total = cursor.execute("SELECT COUNT(*) FROM suppliers").fetchone()[0]
    #     if limit == -1:
    #         cursor.execute("SELECT * FROM suppliers")
    #     else:
    #         cursor.execute("SELECT * FROM suppliers LIMIT ? OFFSET ?", (limit, offset))
    #
    # rows = cursor.fetchall()
    # suppliers = [Supplier(**dict(r)) for r in rows]
    # return HttpListResponse[Supplier](total=total, body=suppliers)


def list_consumers(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Supplier]:
    return _list_suppliers_by_type(offset, limit, filter=filter, type="consumer")
    # conn, cursor = get_connection()
    #
    # if filter is not None:
    #     pattern = f"%{filter}%"
    #     total = cursor.execute(
    #         f"SELECT COUNT(*) FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ?",
    #         ("customer", "both", pattern)
    #     ).fetchone()[0]
    #
    #     if limit == -1:
    #         cursor.execute(
    #             f"SELECT * FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ?",
    #             ("customer", "both", pattern)
    #         )
    #     else:
    #         cursor.execute(
    #             f"SELECT * FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ? LIMIT ? OFFSET ?",
    #             ("customer", "both", pattern, limit, offset)
    #         )
    # else:
    #     total = cursor.execute("SELECT COUNT(*) FROM suppliers WHERE type IN (?, ?)", ("customer", "both")).fetchone()[
    #         0]
    #     if limit == -1:
    #         cursor.execute("SELECT * FROM suppliers WHERE type IN (?, ?)", ("customer", "both"))
    #     else:
    #         cursor.execute("SELECT * FROM suppliers WHERE type IN (?, ?) LIMIT ? OFFSET ?",
    #                        ("customer", "both", limit, offset))
    #
    # rows = cursor.fetchall()
    # customers = [Supplier(**dict(r)) for r in rows]
    # return HttpListResponse[Supplier](total=total, body=customers)


def list_providers(offset: int, limit: int, filter: Optional[str] = None) -> HttpListResponse[Supplier]:
    return _list_suppliers_by_type(offset, limit, filter=filter, type="provider")
    # conn, cursor = get_connection()
    #
    # if filter is not None:
    #     pattern = f"%{filter}%"
    #     total = cursor.execute(
    #         f"SELECT COUNT(*) FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ?",
    #         ("provider", "both", pattern)
    #     ).fetchone()[0]
    #
    #     if limit == -1:
    #         cursor.execute(
    #             f"SELECT * FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ?",
    #             ("provider", "both", pattern)
    #         )
    #     else:
    #         cursor.execute(
    #             f"SELECT * FROM suppliers WHERE type IN (?, ?) AND {filter_expr} LIKE ? LIMIT ? OFFSET ?",
    #             ("provider", "both", pattern, limit, offset)
    #         )
    # else:
    #     total = cursor.execute("SELECT COUNT(*) FROM suppliers WHERE type IN (?, ?)", ("provider", "both")).fetchone()[
    #         0]
    #     if limit == -1:
    #         cursor.execute("SELECT * FROM suppliers WHERE type IN (?, ?)", ("provider", "both"))
    #     else:
    #         cursor.execute("SELECT * FROM suppliers WHERE type IN (?, ?) LIMIT ? OFFSET ?",
    #                        ("provider", "both", limit, offset))
    #
    # rows = cursor.fetchall()
    # providers = [Supplier(**dict(r)) for r in rows]
    # return HttpListResponse[Supplier](total=total, body=providers)
