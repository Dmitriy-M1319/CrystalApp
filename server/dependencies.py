from typing import Annotated
from functools import lru_cache

from config import Settings
from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session

from models.user import User
from db_engine import SessionLocal
from auth.dependencies import get_current_user

@lru_cache
def get_settings():
    return Settings()

def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_token_from_header(token: Annotated[str, Header(min_length=6,
                                                       description='JWT-токен в формате \"Token: jwt-token\"')]):
    try:
        return token.split(':')[1].strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid token format")


def check_permissions(db: Annotated[Session, Depends(get_database_session)],
        token: Annotated[str, Depends(get_token_from_header)]):
    try:
        user = get_current_user(db, token)
    except:
       raise HTTPException(status_code=401, detail="Non authorizated")
    return user


def check_admin_permissions(user: Annotated[User, Depends(check_permissions)]):
    if not user.is_admin:
        raise HTTPException(status_code=401, detail="Non authorizated")
    return user
   
