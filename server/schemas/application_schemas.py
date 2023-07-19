from pydantic import BaseModel

from .product_schemas import ProductGetModel


class ProductApplicationCreate(BaseModel):
    count: int
    provider: str
    product_id: int


class ProductApplicationGet(ProductApplicationCreate):
    id: int
    price: float
    app_status: bool = True
    product: ProductGetModel

    class Config:
        orm_mode = True


