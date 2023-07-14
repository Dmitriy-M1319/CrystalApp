from pydantic import BaseModel

from ..schemas.product_schemas import ProductGetModel


class ProductCart(BaseModel):
    all_sum: float
    products: list[tuple[ProductGetModel, int]]
