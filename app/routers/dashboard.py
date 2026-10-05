from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.stock import StockTransaction
from app.schemas.stock import DashboardResponse

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Get dashboard overview metrics:
    - total products
    - total suppliers
    - total stock quantity
    - low stock products count
    - total stock IN transactions count
    - total stock OUT transactions count
    """
    total_products = db.query(Product).count()
    total_suppliers = db.query(Supplier).count()
    
    total_stock = db.query(func.coalesce(func.sum(Product.quantity), 0)).scalar() or 0
    
    low_stock_products = (
        db.query(Product)
        .filter(Product.quantity < settings.LOW_STOCK_THRESHOLD)
        .count()
    )
    
    total_stock_in = (
        db.query(StockTransaction)
        .filter(StockTransaction.transaction_type == "IN")
        .count()
    )
    
    total_stock_out = (
        db.query(StockTransaction)
        .filter(StockTransaction.transaction_type == "OUT")
        .count()
    )

    return DashboardResponse(
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_stock=int(total_stock),
        low_stock_products=low_stock_products,
        total_stock_in_transactions=total_stock_in,
        total_stock_out_transactions=total_stock_out,
    )
