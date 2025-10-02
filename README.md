Minor Python-ERP-Backend

A simple ERP backend built in Python with SQLite for learning and experimentation.

About

As a PhD student in Mathematics, I was assigned a small Python project 
by my programming instructor. Since it was my first time working with Python,
I decided to challenge myself and build a simple ERP backend from scratch.

I developed this project primarily for fun and to test my skills,
completing it in less than 6 hours. This backend is used to store and manage
users, suppliers, centers, stocks, products, and transactions for a basic ERP system.

Features

Users – Create and manage users with different ranks.

Suppliers – Store supplier information with types (provider, consumer, both).

Centers – Manage business centers with contact details.

Stocks – Link stocks to centers.

Products – Manage products with quantity, purchase/sale price, and expiration date.

Transactions – Record transactions with supplier and product references, type (income/outcome), price, quantity, tax, and discount.

Database – SQLite backend with foreign key constraints.

Data Seeder – Script to populate the database with realistic sample data.

erp-backend/
│── app/
|   |── database/
│   │   │── sql.py                # Connection + execute queries
│   │   │── hash.py               # Password hashing
│   │   │── statements/           # SQL statements for each entity
│   │   │   │── center_statements.py
│   │   │   │── product_statements.py
│   │   │   │── stock_statements.py
│   │   │   │── supplier_statements.py
│   │   │   │── transaction_statements.py
│   │   │   │── user_statements.py
│   │── http_server/
│   │   │── http.py               # Register all routes
│   │   │── __init__.py           # Initialize package
│   │   │── authorization.py      # JWT login & validation
│   │   │── handlers/             # Route handlers
│   │   │   │── http_centers_handler.py
│   │   │   │── http_login_handler.py
│   │   │   │── http_products_handler.py
│   │   │   │── http_stocks_handler.py
│   │   │   │── http_suppliers_handler.py
│   │   │   │── http_transactions_handler.py
│   │   │   │── http_users_handler.py
│   │── entities/                 # Entity models
│   │   │── center.py
│   │   │── http_list_response.py
│   │   │── product.py
│   │   │── stock.py
│   │   │── supplier.py
│   │   │── transaction.py
│   │   │── user.py
│   │── main.py                   # Start FastAPI
│   │── erp.cmd                   # Start command for FastAPI
│   │── erp.db                    # SQLite database


Installation

Clone the repository:

git clone https://github.com/mussab2016/Minor-Python-ERP-Backend.git
cd minor-python-erp-backend

Usage

Run FastAPI backend:
	python app/main.py
or
	./erp.cmd
Access endpoints via http://localhost:8000.

Connect a frontend (like an Angular ERP frontend) to interact with the backend.

License

	MIT License
