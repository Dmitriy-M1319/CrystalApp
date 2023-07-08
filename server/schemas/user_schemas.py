from pydantic import BaseModel


class UserCreate(BaseModel):
    surname: str
    name: str
    email: str
    phone_number: str | None
    password: str
    is_admin: bool


class UserModel(UserCreate):
    id: int


class UserUpdate(BaseModel):
    surname: str
    name: str
    email: str
    phone_number: str | None
