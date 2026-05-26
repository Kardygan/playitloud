from pydantic import BaseModel, ConfigDict, Field

from playitloud.core.constants import (
    MAX_CITY_LENGTH,
    MAX_COUNTRY_CODE_LENGTH,
    MAX_POSTAL_CODE_LENGTH,
    MAX_STREET_LENGTH,
)


class AddressCreate(BaseModel):
    street: str = Field(max_length=MAX_STREET_LENGTH)
    city: str = Field(max_length=MAX_CITY_LENGTH)
    postal_code: str = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: str = Field(max_length=MAX_COUNTRY_CODE_LENGTH)


class AddressRead(BaseModel):
    id: int
    user_id: int
    street: str = Field(max_length=MAX_STREET_LENGTH)
    city: str = Field(max_length=MAX_CITY_LENGTH)
    postal_code: str = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: str = Field(max_length=MAX_COUNTRY_CODE_LENGTH)

    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    street: str = Field(max_length=MAX_STREET_LENGTH)
    city: str = Field(max_length=MAX_CITY_LENGTH)
    postal_code: str = Field(max_length=MAX_POSTAL_CODE_LENGTH)
    country_code: str = Field(max_length=MAX_COUNTRY_CODE_LENGTH)
