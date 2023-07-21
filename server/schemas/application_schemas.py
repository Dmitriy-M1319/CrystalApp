from pydantic import BaseModel, Field

from .product_schemas import ProductGetModel


class ProductApplicationCreate(BaseModel):
    count: int = Field(gt=0)
    provider: str
    product_id: int = Field(gt=0)


class ProductApplicationGet(ProductApplicationCreate):
    id: int
    price: float
    app_status: bool = True
    product: ProductGetModel

    class Config:
        orm_mode = True


