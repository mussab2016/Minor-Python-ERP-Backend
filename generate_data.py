import random
from datetime import datetime, timedelta

from database import init_db, get_connection, hash_password

DB_FILE = "erp-generated.db"

# Initialize schema
conn, cursor = get_connection(DB_FILE)
init_db()
# -----------------------------
# Helpers
# -----------------------------
first_names = ["Ali", "Moussa", "Hassan", "Mourad", "Amina", "Fatima", "Sara", "Nadia", "Omar", "Karim"]
last_names = ["Benali", "Haddad", "Boukhalfa", "Saidi", "Khaled", "Tahar", "Rahmani", "Cherif", "Aziz", "Djebbar"]
cities = ["Algiers", "Oran", "Constantine", "Annaba", "Blida", "Setif", "Tlemcen", "Batna", "Bejaia", "Ghardaia"]
products = ["Milk", "Sugar", "Flour", "Rice", "Oil", "Tea", "Coffee", "Butter", "Juice", "Water"]

def random_date(start_year=2020, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

# -----------------------------
# Users (50)
# -----------------------------
cursor.execute("DELETE FROM users")
for i in range(2, 51):
    name = random.choice(first_names) + " " + random.choice(last_names)
    username = f"user{i}"
    password = hash_password("password")
    rank = random.randint(1, 3)
    cursor.execute(
        "INSERT INTO users (name, username, password, rank) VALUES (?, ?, ?, ?)",
        (name, username, password, rank)
    )

# -----------------------------
# Suppliers (1000+)
# -----------------------------
cursor.execute("DELETE FROM suppliers")
for _ in range(1000):
    firstname = random.choice(first_names)
    lastname = random.choice(last_names)
    supplier_type = random.choice(['provider', 'consumer', 'both'])
    contract_date = random_date(2018, 2025)
    cursor.execute(
        "INSERT INTO suppliers (firstname, lastname, type, contract_date) VALUES (?, ?, ?, ?)",
        (firstname, lastname, supplier_type, contract_date)
    )

# -----------------------------
# Centers (1000+)
# -----------------------------
cursor.execute("DELETE FROM centers")
for i in range(1000):
    name = f"Center-{i}"
    city = random.choice(cities)
    address = f"Street {random.randint(1, 200)}"
    phone = f"+213{random.randint(600000000, 799999999)}"
    email = f"center{i}@mail.com"
    cursor.execute(
        "INSERT INTO centers (name, city, address, phone, email) VALUES (?, ?, ?, ?, ?)",
        (name, city, address, phone, email)
    )

# -----------------------------
# Stocks (1000+)
# -----------------------------
cursor.execute("DELETE FROM stocks")
cursor.execute("SELECT id FROM centers")
center_ids = [row[0] for row in cursor.fetchall()]
for i in range(1000):
    name = f"Stock-{i}"
    city = random.choice(cities)
    address = f"Warehouse Road {random.randint(1, 200)}"
    center_id = random.choice(center_ids)
    cursor.execute(
        "INSERT INTO stocks (name, city, address, center_id) VALUES (?, ?, ?, ?)",
        (name, city, address, center_id)
    )

# -----------------------------
# Products (1200+)
# -----------------------------
cursor.execute("DELETE FROM products")
cursor.execute("SELECT id FROM stocks")
stock_ids = [row[0] for row in cursor.fetchall()]
for i in range(1200):
    name = random.choice(products) + f"-{i}"
    description = f"{name} description"
    stock_id = random.choice(stock_ids)
    quantity = random.uniform(1, 500)  # REAL field
    expiration_date = random_date(2025, 2030)
    purchase_price = random.randint(10, 200)
    sale_price = purchase_price + random.randint(1, 50)
    cursor.execute(
        """INSERT INTO products 
        (name, description, stock_id, quantity, expiration_date, purchase_price, sale_price) 
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (name, description, stock_id, quantity, expiration_date, purchase_price, sale_price)
    )

# -----------------------------
# Transactions (1500+)
# -----------------------------
cursor.execute("DELETE FROM transactions")
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]
for _ in range(1500):
    supplier_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    date = random_date(2022, 2025) + " 12:00:00"
    trans_type = random.choice([1, -1])
    price = random.randint(50, 500)
    quantity = random.uniform(1, 100)
    tax = random.uniform(0, 20)
    discount = random.uniform(0, 10)
    cursor.execute(
        """INSERT INTO transactions 
        (supplier_id, date, product_id, type, price, quantity, tax, discount) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (supplier_id, date, product_id, trans_type, price, quantity, tax, discount)
    )

# Commit
conn.commit()
print("Database populated with sample data ✅")
