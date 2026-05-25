from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
    
class UserUpdateInfo(BaseModel):
    first_name: str
    last_name: str