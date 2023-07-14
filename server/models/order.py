from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Float 
from sqlalchemy.orm import relationship

from ..db_engine import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    client_address = Column(String)
    is_delivery = Column(Boolean, default=False)
    payment_type = Column(String)
    order_status = Column(Boolean, default=True)
    client_id = Column(Integer, ForeignKey('users.id'))

    client = relationship('User', back_populates='orders')
    orders_products = relationship('OrderProduct', back_populates='order')


class OrderProduct(Base):
    __tablename__  ='orders_products'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    product_count = Column(Integer)

    order = relationship('Order', back_populates='orders_products')
    product = relationship('Product', back_populates='orders_products')

