from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    """Base schema for Product."""

    name: str = Field(..., min_length=1, description="Product name")
    sku: str = Field(..., min_length=1, description="Unique Stock Keeping Unit")
    category: str = Field(..., min_length=1, description="Product category")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Product price (must be >= 0)")
    quantity: int = Field(default=0, ge=0, description="Available stock quantity (must be >= 0)")
    supplier_id: Optional[int] = Field(None, description="Optional ID of associated supplier")


class ProductCreate(ProductBase):
    """Schema for creating a new product."""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""

    name: Optional[str] = Field(None, min_length=1)
    sku: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[int] = None


class ProductResponse(ProductBase):
    """Schema for product response."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
