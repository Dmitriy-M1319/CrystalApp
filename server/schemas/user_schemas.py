from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    surname: str
    name: str
    email: EmailStr
    phone_number: str | None
    password: str
    is_admin: bool


class UserModel(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    surname: str
    name: str
    email: EmailStr
    phone_number: str | None
