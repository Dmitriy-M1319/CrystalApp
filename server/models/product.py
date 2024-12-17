from sqlalchemy import Column, String, Integer, Float 
from sqlalchemy.orm import relationship

from db_engine import Base


class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    company = Column(String)
    client_price = Column(Float)
    purchase_price = Column(Float)
    count_on_warehouse = Column(Integer)

    orders_products = relationship('OrderProduct', back_populates='product')
    applications = relationship('ProductApplication', back_populates='product')
