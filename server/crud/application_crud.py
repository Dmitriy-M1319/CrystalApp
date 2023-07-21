from sqlalchemy.orm import Session

from ..models.application import ProductApplication
from ..schemas.application_schemas import *
from ..exceptions import RowNotFoundException
from .product_crud import get_product, add_new_product_count


def get_all_applications(database: Session):
    return database.query(ProductApplication).all()


def get_application(database: Session, app_id: int) -> ProductApplication:
    app = database.query(ProductApplication).filter(ProductApplication.id == app_id).first()
    if app is None:
        raise RowNotFoundException('ProductApplication', str(app_id))
    else:
        return app


def create_application(database: Session, 
                       app_part: ProductApplicationCreate) -> ProductApplication:
    new_app = ProductApplication(**app_part.dict())
    product = get_product(database, app_part.product_id)
    new_app.price = app_part.count * product.purchase_price
    database.add(new_app)
    database.commit()
    database.refresh(new_app)
    return new_app


def close_application(database: Session, app_id: int) -> ProductApplication:
    app = get_application(database, app_id)
    app.app_status = False
    database.commit()
    add_new_product_count(database, app.product_id, app.count) 
    return app
