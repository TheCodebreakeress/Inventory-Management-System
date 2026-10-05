from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SupplierBase(BaseModel):
    """Base schema for Supplier."""

    name: str = Field(..., min_length=1, description="Supplier name")
    email: str = Field(..., min_length=1, description="Supplier email address")
    phone: str = Field(..., min_length=1, description="Supplier contact phone")
    address: Optional[str] = Field(None, description="Supplier physical address")


class SupplierCreate(SupplierBase):
    """Schema for creating a new supplier."""

    pass


class SupplierUpdate(BaseModel):
    """Schema for updating an existing supplier."""

    name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = Field(None, min_length=1)
    phone: Optional[str] = Field(None, min_length=1)
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    """Schema for supplier response."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
