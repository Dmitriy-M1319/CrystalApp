from typing import Type

from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas import user_schemas
from ..exceptions import RowNotFoundException


def get_user(database: Session, user_id: int) -> Type[User]:
    user = database.query(User).filter(User.id == user_id).first()
    if not user:
        raise RowNotFoundException('User', str(user_id))
    else:
        return user


def get_user_by_email(database: Session, email: str) -> Type[User]:
    user = database.query(User).filter(User.email == email).first()
    if not user:
        raise RowNotFoundException('User', email)
    else:
        return user


def create_user(database: Session, user: user_schemas.UserCreate) -> User:
    new_user = User(**user.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


def update_user(database: Session, user_id: int, user_data: user_schemas.UserUpdate | User) -> Type[User]:
    existing_user = get_user(database, user_id)
    existing_user.surname = user_data.surname
    existing_user.name = user_data.name
    existing_user.email = user_data.email
    existing_user.phone_number = user_data.phone_number

    database.commit()
    database.refresh(existing_user)
    return existing_user


def delete_user(database: Session, user_id: int):
    existing_user = get_user(database, user_id)
    database.delete(existing_user)
    database.commit()
