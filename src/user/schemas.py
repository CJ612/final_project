from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    name: str|None
    age: int|None
    email: EmailStr|None

class UserCreate(UserBase):
    password: str
    
class UserUpdate(UserBase):
    name: Optional[str]
    age: Optional[int]
    password: Optional[str]
    email: Optional[EmailStr]
    
class UserInOut(UserBase):
    id: int

    class Config:
        from_attributes = True