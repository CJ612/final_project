from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    name: str|None
    age: int|None
    email: EmailStr|None


class UserCreate(UserBase):
    password: str


class UserInOut(UserBase):
    id: int

    class Config:
        # from_attributes = True
        orm_mode = True