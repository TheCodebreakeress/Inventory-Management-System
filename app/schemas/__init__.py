from app.schemas.supplier import SupplierBase, SupplierCreate, SupplierUpdate, SupplierResponse
from app.schemas.product import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.schemas.stock import StockTransactionCreate, StockTransactionResponse, DashboardResponse

__all__ = [
    "SupplierBase",
    "SupplierCreate",
    "SupplierUpdate",
    "SupplierResponse",
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "StockTransactionCreate",
    "StockTransactionResponse",
    "DashboardResponse",
]
