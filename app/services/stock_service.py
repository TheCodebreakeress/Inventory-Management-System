from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.stock import StockTransaction


class StockService:
    """Service class handling stock transactions and business rules."""

    @staticmethod
    def process_stock_in(db: Session, product_id: int, quantity: int) -> StockTransaction:
        """
        Process incoming stock for a product.
        Increases the product's quantity and records a StockTransaction.
        """
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock quantity must be greater than 0",
            )

        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        previous_quantity = product.quantity
        new_quantity = previous_quantity + quantity
        product.quantity = new_quantity

        transaction = StockTransaction(
            product_id=product.id,
            transaction_type="IN",
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        db.refresh(product)
        return transaction

    @staticmethod
    def process_stock_out(db: Session, product_id: int, quantity: int) -> StockTransaction:
        """
        Process outgoing stock for a product.
        Decreases the product's quantity if sufficient stock exists, and records a StockTransaction.
        """
        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock quantity must be greater than 0",
            )

        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        if product.quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Insufficient stock for product '{product.name}'. "
                    f"Available: {product.quantity}, Requested: {quantity}"
                ),
            )

        previous_quantity = product.quantity
        new_quantity = previous_quantity - quantity
        product.quantity = new_quantity

        transaction = StockTransaction(
            product_id=product.id,
            transaction_type="OUT",
            quantity=quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        db.refresh(product)
        return transaction

    @staticmethod
    def get_transactions(db: Session, product_id: Optional[int] = None) -> List[StockTransaction]:
        """Retrieve stock transactions, optionally filtered by product_id."""
        query = db.query(StockTransaction)
        if product_id is not None:
            query = query.filter(StockTransaction.product_id == product_id)
        return query.order_by(StockTransaction.created_at.desc()).all()

    @staticmethod
    def get_low_stock_products(db: Session, threshold: int) -> List[Product]:
        """
        Retrieve products whose quantity is strictly less than the low stock threshold.
        """
        return (
            db.query(Product)
            .filter(Product.quantity < threshold)
            .order_by(Product.quantity.asc())
            .all()
        )
