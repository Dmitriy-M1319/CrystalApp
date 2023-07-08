from sqlalchemy.orm import Session

from ..models.product import Product
from ..schemas.product_schemas import ProductCreateOrUpdateModel


def get_products(database: Session, company_filter: str | None = None):
    products = database.query(Product).order_by('id')
    if company_filter:
        return products.filter(Product.company == company_filter).all()
    else:
        return products.all()


def get_product(database: Session, product_id: int):
    return database.query(Product).filter(Product.id == product_id).first()


def create_product(database: Session, product: ProductCreateOrUpdateModel):
    new_product = Product(**product.dict())
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


def update_product(database: Session,
                   product_id: int,
                   product_data: ProductCreateOrUpdateModel):
    updated_product = database.query(Product).filter(Product.id == product_id).first()
    if not updated_product:
        raise Exception('Product not found')
    updated_product.name = product_data.name
    updated_product.company = product_data.company
    updated_product.client_price = product_data.client_price
    updated_product.purchase_price = product_data.purchase_price
    updated_product.count_on_warehouse = product_data.count_on_warehouse

    database.commit()
    database.refresh(updated_product)
    return updated_product


def delete_product(database: Session, product_id: int):
    deleted_product = database.query(Product).filter(Product.id == product_id).first()
    if not deleted_product:
        raise Exception('Product not found')
    database.delete(deleted_product)
    database.commit()
