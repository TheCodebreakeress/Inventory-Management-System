from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class StockTransactionCreate(BaseModel):
    """Schema for creating a stock transaction (IN or OUT)."""

    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., gt=0, description="Quantity to adjust (must be > 0)")


class StockTransactionResponse(BaseModel):
    """Schema for stock transaction response."""

    id: int
    product_id: int
    transaction_type: str
    quantity: int
    previous_quantity: int
    new_quantity: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    """Schema for system overview dashboard statistics."""

    total_products: int
    total_suppliers: int
    total_stock: int
    low_stock_products: int
    total_stock_in_transactions: int
    total_stock_out_transactions: int
