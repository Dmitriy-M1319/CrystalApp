from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Float 
from sqlalchemy.orm import relationship

from ..db_engine import Base


class ProductApplication(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, index=True)
    count = Column(Integer)
    provider = Column(String)
    price = Column(Float)
    app_status = Column(Boolean, default=True)
    product_id = Column(Integer, ForeignKey('products.id'))

    product = relationship('Product', back_populates='applications')
