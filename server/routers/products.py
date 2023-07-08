import sqlalchemy.exc
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_database_session
from ..schemas import product_schemas
from ..crud import product_crud


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/', response_model=list[product_schemas.ProductGetModel])
def get_product_catalog(db: Annotated[Session, Depends(get_database_session)],
                        company_filter: str | None = None):
    return product_crud.get_products(db, company_filter)


@router.get('/{product_id}', response_model=product_schemas.ProductGetModel)
def get_product_by_id(db: Annotated[Session, Depends(get_database_session)],
                      product_id: int):
    product = product_crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        return product


@router.post('/', response_model=product_schemas.ProductGetModel)
def create_product(db: Annotated[Session, Depends(get_database_session)],
                   product: product_schemas.ProductCreateOrUpdateModel):
    new_product = product_crud.create_product(db, product)
    return new_product


@router.put('/{product_id}', response_model=product_schemas.ProductGetModel)
def update_product(db: Annotated[Session, Depends(get_database_session)],
                   product_id: int, product_data: product_schemas.ProductCreateOrUpdateModel):
    try:
        return product_crud.update_product(db, product_id, product_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@router.delete('/{product_id}', response_model=None)
def remove_product(db: Annotated[Session, Depends(get_database_session)],
                   product_id: int):
    try:
        return product_crud.delete_product(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
