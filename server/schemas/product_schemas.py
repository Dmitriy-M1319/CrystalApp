from pydantic import BaseModel, Field


class ProductCreateOrUpdateModel(BaseModel):
    name: str
    company: str
    client_price: float = Field(gt=0)
    purchase_price: float = Field(gt=0)
    count_on_warehouse: int = Field(gt=0)


class ProductGetModel(ProductCreateOrUpdateModel):
    id: int

    class Config:
        orm_mode = True

