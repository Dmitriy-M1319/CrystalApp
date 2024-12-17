from datetime import timedelta, datetime
from typing import Type, Annotated

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from crud import user_crud
from schemas import auth_schemas
from models.user import User
from schemas.user_schemas import UserCreate
from .settings import *


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_user_password(user: UserCreate):
    user.password = pwd_context.hash(user.password)
    return user


def authenticate(database: Session, data: auth_schemas.AuthenticateUserData) -> Type[User] | bool:
    user = user_crud.get_user_by_email(database, data.email)
    if not verify_passwords(data.password, user.password):
        return False
    return user


def verify_passwords(plain, hashed):
    return pwd_context.verify(plain, hashed)


def generate_token(token_data: dict, expires_delta: timedelta | None = None):
    encoded = token_data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encoded.update({"exp": expire})
    jwt_token = jwt.encode(encoded, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def get_current_user(database: Session, token: str):
    credentials_exc = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = decoded.get('sub')
        if email is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc

    current_user = user_crud.get_user_by_email(database, email)
    return current_user


def reset_user_password(database: Session,
                   token: str,
                   user_data: auth_schemas.PasswordUpdate):
    current_user = get_current_user(database, token)
    current_user.password = pwd_context.hash(user_data.new_password)
    database.commit()

