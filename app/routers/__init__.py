from app.routers.products import router as products_router
from app.routers.suppliers import router as suppliers_router
from app.routers.stock import router as stock_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "products_router",
    "suppliers_router",
    "stock_router",
    "dashboard_router",
]
