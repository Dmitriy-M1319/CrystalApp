from fastapi.security import OAuth2PasswordBearer

from .db_engine import SessionLocal
from .schemas.user_schemas import UserCreate


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def hash_user_password(user: UserCreate):
    # здесь сразу хешируем пароль у пользователя
    return user
