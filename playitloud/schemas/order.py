from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from playitloud.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    album_id: int
    quantity: int = Field(gt=0)


class OrderItemRead(BaseModel):
    album_id: int
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    address_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderRead(BaseModel):
    id: int
    user_id: int
    address_id: int
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    updated_at: datetime
    order_items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
