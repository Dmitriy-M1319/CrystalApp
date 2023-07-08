from pydantic import BaseModel


class ProductCreateOrUpdateModel(BaseModel):
    name: str
    company: str
    client_price: float
    purchase_price: float
    count_on_warehouse: int


class ProductGetModel(ProductCreateOrUpdateModel):
    id: int

    class Config:
        orm_mode = True
