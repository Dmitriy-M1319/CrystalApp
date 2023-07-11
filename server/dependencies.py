from typing import Annotated

from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session

from .models.user import User
from .db_engine import SessionLocal
from .auth.dependencies import get_current_user


def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_token_from_header(token: Annotated[str, Header(min_length=6)]):
    return token.split(':')[1].strip()


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
   




