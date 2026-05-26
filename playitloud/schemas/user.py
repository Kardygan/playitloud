from pydantic import BaseModel, ConfigDict, EmailStr, Field

from playitloud.core.constants import (
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
    MAX_PASSWORD_HASH_LENGTH,
)


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(max_length=MAX_PASSWORD_HASH_LENGTH)
    first_name: str = Field(max_length=MAX_FIRST_NAME_LENGTH)
    last_name: str = Field(max_length=MAX_LAST_NAME_LENGTH)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str = Field(max_length=MAX_FIRST_NAME_LENGTH)
    last_name: str = Field(max_length=MAX_LAST_NAME_LENGTH)

    model_config = ConfigDict(from_attributes=True)

class UserUpdateInfo(BaseModel):
    first_name: str = Field(max_length=MAX_FIRST_NAME_LENGTH)
    last_name: str = Field(max_length=MAX_LAST_NAME_LENGTH)
