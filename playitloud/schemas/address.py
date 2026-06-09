from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from playitloud.core.constants import (
    MAX_CITY_LENGTH,
    MAX_COUNTRY_CODE_LENGTH,
    MAX_POSTAL_CODE_LENGTH,
    MAX_STREET_LENGTH,
)
from playitloud.schemas.types import NonBlankStr


def _normalize_country_code(value: str) -> str:
    if isinstance(value, str):
        return value.strip().upper()
    return value


CountryCode = Annotated[
    str,
    BeforeValidator(_normalize_country_code),
    Field(max_length=MAX_COUNTRY_CODE_LENGTH),
]


class AddressCreate(BaseModel):
    street: NonBlankStr = Field(max_length=MAX_STREET_LENGTH)
    city: NonBlankStr = Field(max_length=MAX_CITY_LENGTH)
    postal_code: NonBlankStr = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: CountryCode


class AddressRead(BaseModel):
    id: int
    user_id: int
    street: str = Field(max_length=MAX_STREET_LENGTH)
    city: str = Field(max_length=MAX_CITY_LENGTH)
    postal_code: str = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: str = Field(max_length=MAX_COUNTRY_CODE_LENGTH)

    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    street: NonBlankStr = Field(max_length=MAX_STREET_LENGTH)
    city: NonBlankStr = Field(max_length=MAX_CITY_LENGTH)
    postal_code: NonBlankStr = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: CountryCode
