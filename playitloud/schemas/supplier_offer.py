from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from playitloud.core.constants import MAX_PRICE


class SupplierOfferCreate(BaseModel):
    album_id: int
    unit_price: Decimal = Field(gt=0, le=MAX_PRICE, max_digits=10, decimal_places=2)


class SupplierOfferRead(BaseModel):
    supplier_id: int
    album_id: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class SupplierOfferUpdate(BaseModel):
    unit_price: Decimal = Field(gt=0, le=MAX_PRICE, max_digits=10, decimal_places=2)
