from typing import Type

from sqlalchemy.orm import Session

from ..crud import user_crud
from ..schemas import user_schemas, auth_schemas
from ..models.user import User
from .dependencies import verify_passwords


def authenticate(database: Session, data: auth_schemas.AuthenticateUserData) -> Type[User] | bool:
    user = user_crud.get_user_by_email(database, data.email)
    if not verify_passwords(data.password, user.password):
        return False
    return user


def generate_token():
    pass