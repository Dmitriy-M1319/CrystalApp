from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import RowNotFoundException
from ..dependencies import *
from ..schemas import product_schemas, extra_schemas
from ..crud import product_crud


router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.get('/', response_model=list[product_schemas.ProductGetModel])
def get_product_catalog(db: Annotated[Session, Depends(get_database_session)],
                        company_filter: str | None = None):
    return product_crud.get_products(db, company_filter)


@router.get('/{product_id}',
            response_model=product_schemas.ProductGetModel,
            responses={404: {'model': extra_schemas.Message}})
def get_product_by_id(db: Annotated[Session, Depends(get_database_session)],
                      product_id: int):
    try:
        return product_crud.get_product(db, product_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)


@router.post('/', response_model=product_schemas.ProductGetModel,
             dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
             responses={400: {'model': extra_schemas.Message}})
def create_product(db: Annotated[Session, Depends(get_database_session)],
                   product: product_schemas.ProductCreateOrUpdateModel):
    try:
        return product_crud.create_product(db, product)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.put('/{product_id}', response_model=product_schemas.ProductGetModel,
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
            responses={404: {'model': extra_schemas.Message},
                       400: {'model': extra_schemas.Message}})
def update_product(db: Annotated[Session, Depends(get_database_session)],
                   product_id: int, product_data: product_schemas.ProductCreateOrUpdateModel):
    try:
        return product_crud.update_product(db, product_id, product_data)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.delete('/{product_id}', response_model=None,
               dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
               responses={404: {'model': extra_schemas.Message}})
def remove_product(db: Annotated[Session, Depends(get_database_session)],
                   product_id: int):
    try:
        return product_crud.delete_product(db, product_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
