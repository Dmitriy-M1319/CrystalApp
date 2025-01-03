from pydantic import BaseModel

from .product_schemas import ProductGetModel
from .user_schemas import UserModel


class OrderCreate(BaseModel):
    client_address: str
    is_delivery: bool = False
    payment_type: str


class OrderProduct(BaseModel):
    product: ProductGetModel
    count: int


class OrderGetForClient(OrderCreate):
    id: int
    total_price: float
    order_status: bool = True
    orders_products: list[OrderProduct]

    class Config:
        orm_mode = True


class OrderGetForAdmin(OrderGetForClient):
    client: UserModel
    
class GetOrdersReport(BaseModel):
    from_date: str
    to_date: str
