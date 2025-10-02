# http.py
from fastapi import APIRouter  # Router class to register and group endpoints

# Import all handlers (each handler defines its own sub-router)
from .handlers import (
    http_users_handler,
    http_suppliers_handler,
    http_products_handler,
    http_transactions_handler,
    http_centers_handler,
    http_stocks_handler,
    http_login_handler,
)

# Create a main router to register all entity-specific routers
api_router = APIRouter()

# Register sub-routers
# include_router parameters:
# - router:        The APIRouter instance from the handler (contains endpoints).
# - prefix:        A URL prefix for all routes in this router (ex: "/users" → GET /users/).
# - tags:          Labels used in Swagger UI to group related endpoints visually.
# - dependencies:  (optional) List of dependencies applied to all routes in this router.
# - responses:     (optional) Custom response descriptions for the whole router.
api_router.include_router(http_login_handler.router, prefix="/login", tags=["Login"])
api_router.include_router(http_users_handler.router, prefix="/users", tags=["Users"])
api_router.include_router(http_centers_handler.router, prefix="/centers", tags=["Centers"])
api_router.include_router(http_stocks_handler.router, prefix="/stocks", tags=["Stocks"])
api_router.include_router(http_suppliers_handler.router, prefix="/suppliers", tags=["Suppliers"])
api_router.include_router(http_products_handler.router, prefix="/products", tags=["Products"])
api_router.include_router(http_transactions_handler.router, prefix="/transactions", tags=["Transactions"])
