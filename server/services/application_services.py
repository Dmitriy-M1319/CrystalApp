from sqlalchemy.orm import Session

from crud.product_crud import get_product
from models.application import ProductApplication


def reformat_app(database: Session, app: ProductApplication):
    application = app.__dict__
    application['product'] = get_product(database, app.product_id)
    return application 


def reformat_applications(database: Session, applications):
    result = []
    for app in applications:
        result.append(reformat_app(database, app))
    return result

