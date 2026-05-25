from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    street: str
    city: str
    postal_code: str
    country_code: str


class AddressRead(BaseModel):
    id: int
    user_id: int
    street: str
    city: str
    postal_code: str
    country_code: str

    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    street: str
    city: str
    postal_code: str
    country_code: str
