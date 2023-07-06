from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO: Выбрать базу данных для использования
SQLALCHEMY_DATABASE_URL='sqlite:///./temp_db.sqlite3'

engine = create_engine(
    # использование connect_args необходимо только для SQLite
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread', False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
