from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from playitloud.models.supplier_order import RestockStatus


class SupplierOrderItemCreate(BaseModel):
    album_id: int
    quantity: int = Field(gt=0)


class SupplierOrderItemRead(BaseModel):
    album_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class SupplierOrderCreate(BaseModel):
    items: list[SupplierOrderItemCreate] = Field(min_length=1)


class SupplierOrderRead(BaseModel):
    id: int
    supplier_id: int
    status: RestockStatus
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    supplier_order_items: list[SupplierOrderItemRead]

    model_config = ConfigDict(from_attributes=True)


class RestockStatusUpdate(BaseModel):
    status: RestockStatus
