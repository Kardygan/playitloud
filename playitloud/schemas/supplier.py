from pydantic import BaseModel, ConfigDict, EmailStr, Field

from playitloud.core.constants import MAX_SUPPLIER_NAME_LENGTH
from playitloud.schemas.types import NonBlankStr


class SupplierCreate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_SUPPLIER_NAME_LENGTH)
    contact_email: EmailStr | None = None


class SupplierRead(BaseModel):
    id: int
    name: str
    contact_email: EmailStr | None

    model_config = ConfigDict(from_attributes=True)


class SupplierUpdate(BaseModel):
    name: NonBlankStr = Field(max_length=MAX_SUPPLIER_NAME_LENGTH)
    contact_email: EmailStr | None = None
