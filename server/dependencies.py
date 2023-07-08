from fastapi.security import OAuth2PasswordBearer

from .db_engine import SessionLocal


oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


