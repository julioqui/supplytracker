from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

class SupplyBase(BaseModel):
    name: str
    category: Optional[str] = None
    unit: str
    cost_per_unit: float
    stock_quantity: float
    min_stock: float

    @field_validator("stock_quantity")
    def validate_stock_not_negative(cls, v):
        if v < 0:
            raise ValueError("stock_quantity cannot be negative")
        return v

    @field_validator("cost_per_unit")
    def validate_cost_not_negative(cls, v):
        if v < 0:
            raise ValueError("cost_per_unit cannot be negative")
        return v

    # ✔ Pydantic v2-compliant cross-field validation
    @model_validator(mode="after")
    def validate_min_stock(self):
        if self.min_stock > self.stock_quantity:
            raise ValueError("min_stock cannot exceed stock_quantity")
        return self


class SupplyCreate(SupplyBase):
    pass


class SupplyUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    cost_per_unit: Optional[float] = None
    stock_quantity: Optional[float] = None
    min_stock: Optional[float] = None

    @field_validator("stock_quantity")
    def validate_stock_not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("stock_quantity cannot be negative")
        return v

    @field_validator("cost_per_unit")
    def validate_cost_not_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("cost_per_unit cannot be negative")
        return v

    # ✔ Cross-field validation for update inputs
    @model_validator(mode="after")
    def validate_min_stock(self):
        if (
            self.min_stock is not None and
            self.stock_quantity is not None and
            self.min_stock > self.stock_quantity
        ):
            raise ValueError("min_stock cannot exceed stock_quantity")
        return self


class SupplyResponse(SupplyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
