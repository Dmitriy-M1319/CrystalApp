from sqlalchemy.orm import Session

from ..models.product import Product
from ..schemas.product_schemas import ProductCreateOrUpdateModel
from ..exceptions import RowNotFoundException


def get_products(database: Session, company_filter: str | None = None):
    products = database.query(Product).order_by('id')
    if company_filter:
        return products.filter(Product.company == company_filter).all()
    else:
        return products.all()


def get_product(database: Session, product_id: int):
    product = database.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise RowNotFoundException('Product', str(product_id))
    else:
        return product


def create_product(database: Session, product: ProductCreateOrUpdateModel):
    new_product = Product(**product.dict())
    database.add(new_product)
    database.commit()
    database.refresh(new_product)
    return new_product


def add_new_product_count(database, Session, 
                          product_id: int, product_count: int):
    product = get_product(database, product_id)
    product.count_on_warehouse += product_count
    database.commit()


def remove_products_from_warehouse(database: Session,
                                   product_id: int, product_count: int):
    product = get_product(database, product_id)
    if product_count > product.count_on_warehouse:
        raise ValueError('Failed to remove products from warehouse: too many removed products')
    product.count_on_warehouse -= product_count
    database.commit()


def update_product(database: Session,
                   product_id: int,
                   product_data: ProductCreateOrUpdateModel):
    updated_product = get_product(database, product_id)
    updated_product.name = product_data.name
    updated_product.company = product_data.company
    updated_product.client_price = product_data.client_price
    updated_product.purchase_price = product_data.purchase_price
    updated_product.count_on_warehouse = product_data.count_on_warehouse

    database.commit()
    database.refresh(updated_product)
    return updated_product


def delete_product(database: Session, product_id: int):
    deleted_product = get_product(database, product_id)
    database.delete(deleted_product)
    database.commit()
