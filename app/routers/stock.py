from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.schemas.product import ProductResponse
from app.schemas.stock import StockTransactionCreate, StockTransactionResponse
from app.services.stock_service import StockService

router = APIRouter(prefix="/api/stock", tags=["Stock"])


@router.post("/in", response_model=StockTransactionResponse)
def stock_in(
    data: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Increase product stock quantity and log an IN transaction.
    """
    return StockService.process_stock_in(
        db=db,
        product_id=data.product_id,
        quantity=data.quantity,
    )


@router.post("/out", response_model=StockTransactionResponse)
def stock_out(
    data: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Decrease product stock quantity and log an OUT transaction.
    Returns 400 if requested quantity exceeds current stock.
    """
    return StockService.process_stock_out(
        db=db,
        product_id=data.product_id,
        quantity=data.quantity,
    )


@router.get("", response_model=List[StockTransactionResponse])
def get_stock_transactions(
    product_id: Optional[int] = Query(None, description="Optional product ID to filter transactions"),
    db: Session = Depends(get_db),
):
    """
    Retrieve stock transaction history, optionally filtered by product_id.
    """
    return StockService.get_transactions(db=db, product_id=product_id)


@router.get("/low", response_model=List[ProductResponse])
def get_low_stock(db: Session = Depends(get_db)):
    """
    Retrieve all products whose stock is below LOW_STOCK_THRESHOLD.
    """
    return StockService.get_low_stock_products(db=db, threshold=settings.LOW_STOCK_THRESHOLD)
