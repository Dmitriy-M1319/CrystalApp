from .db_engine import SessionLocal


def get_database_session():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
