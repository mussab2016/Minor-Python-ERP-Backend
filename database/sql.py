# sql.py
import sqlite3
import threading

from .hash import hash_password

DB_FILE = "erp.db"


# Global lock instance
db_lock = threading.Lock()

# -----------------------------
# Persistent connection
# -----------------------------
conn = None
cursor = None


def get_connection(name: str = DB_FILE) -> sqlite3.Connection:
    """Return the persistent connection and cursor."""
    global conn, cursor
    if conn is None:
        conn = sqlite3.connect(name, check_same_thread=False)
        conn.row_factory = sqlite3.Row  # optional, dict-like access
        cursor = conn.cursor()
    return conn, cursor


def init_db():
    """Initialize the database if it doesn't exist."""
    # if os.path.exists(DB_FILE):
    #     print(f"Database {DB_FILE} already exists, skipping initialization.")
    #     return

    conn, cursor = get_connection()

    # -----------------------------
    # Users table
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users
                   (
                       id       INTEGER PRIMARY KEY AUTOINCREMENT,
                       name     TEXT NOT NULL,
                       username TEXT NOT NULL UNIQUE,
                       password TEXT NOT NULL,
                       rank     INTEGER DEFAULT 1
                   )
                   """)

    # Hash the initial password
    password_plain = "123456789"
    hashed_pw = hash_password(password_plain)

    # Insert default Manager user only if table is empty
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()["count"] == 0:
        password_hashed = hash_password("123456789")
        cursor.execute("""
                       INSERT INTO users (name, username, password, rank)
                       VALUES (?, ?, ?, ?)
                       """, ("Admin", "Manager", password_hashed, 3))

    # # Insert initial Manager user
    # cursor.execute("""
    #                INSERT INTO users (name, username, password, rank)
    #                VALUES (?, ?, ?, ?) WHERE NOT EXISTS (SELECT 1 FROM users);
    #                """, ("Admin", "Manager", hashed_pw, 3))
    #
    # # -----------------------------
    # Suppliers table
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS suppliers
                   (
                       id            INTEGER PRIMARY KEY AUTOINCREMENT,
                       firstname     TEXT NOT NULL,
                       lastname      TEXT NOT NULL,
                       type          TEXT NOT NULL CHECK (type IN ('provider', 'consumer', 'both')),
                       contract_date DATE NOT NULL
                   )
                   """)

    # -----------------------------
    # Centers table
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS centers
                   (
                       id      INTEGER PRIMARY KEY AUTOINCREMENT,
                       name    TEXT NOT NULL,
                       city    TEXT NOT NULL,
                       address TEXT NOT NULL,
                       phone   TEXT,
                       email   TEXT
                   )
                   """)

    # -----------------------------
    # Stocks table  #ON DELETE CASCADE
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS stocks
                   (
                       id        INTEGER PRIMARY KEY AUTOINCREMENT,
                       name      TEXT    NOT NULL,
                       city      TEXT    NOT NULL,
                       address   TEXT    NOT NULL,
                       center_id INTEGER NOT NULL,
                       FOREIGN KEY (center_id) REFERENCES centers (id)
                   )
                   """)

    # -----------------------------
    # Products table
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS products
                   (
                       id             INTEGER PRIMARY KEY AUTOINCREMENT,
                       name           TEXT    NOT NULL,
                       description    TEXT,
                       stock_id       INTEGER NOT NULL,
                       quantity       REAL DEFAULT 0,
                       expiration_date     DATE    NOT NULL,
                       purchase_price REAL DEFAULT 0,
                       sale_price     REAL DEFAULT 0,
                       FOREIGN KEY (stock_id) REFERENCES stocks (id)
                   )
                   """)

    # -----------------------------
    # Transactions table
    # -----------------------------
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions
                   (
                       id       INTEGER PRIMARY KEY AUTOINCREMENT,
                       supplier_id  INTEGER  NOT NULL,
                       date     DATETIME NOT NULL,
                       product_id  INTEGER NOT NULL,
                       type     INTEGER  NOT NULL CHECK (type IN (1, -1)),
                       price    REAL  NOT NULL,
                       quantity REAL  NOT NULL,
                       tax      REAL DEFAULT 0,
                       discount REAL DEFAULT 0,
                       FOREIGN KEY (supplier_id) REFERENCES users (id),
                       FOREIGN KEY (product_id) REFERENCES products (id)
                   )
                   """)

    conn.commit()
    print(f"Database {DB_FILE} initialized successfully.")

# def close_connection():
#     """Close the persistent connection when the app stops."""
#     global conn
#     if conn:
#         conn.commit()
#         conn.close()
#         conn = None
