from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from db_engine import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

    orders = relationship('Order', back_populates='client', lazy='dynamic')

