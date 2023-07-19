#TODO: Сделать валидацию на все ключи и некоторые поля

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from ..crud import application_crud
from ..schemas.application_schemas import ProductApplicationCreate, \
    ProductApplicationGet
from ..services.order_services import reformat_orders_from_db, \
        reformat_order
from ..services.application_services import *
from ..schemas.order_schemas import *
from ..schemas.extra_schemas import *
from ..exceptions import RowNotFoundException
from ..crud import order_crud
from ..dependencies import *


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


@router.get('/orders',
            response_model=list[OrderGetForAdmin],
            responses={
                400: {'model': Message},
                401: {'model': Message},
                },
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def get_orders_for_admin(db: Annotated[Session, Depends(get_database_session)]):
    return reformat_orders_from_db(db, order_crud.get_all_orders(db))


@router.delete('/orders/{order_id}',
               responses={
                   400: {'model': Message},
                   401: {'model': Message},
                   404: {'model': Message},
                },
               response_model=OrderGetForAdmin,
               dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def close_order(db: Annotated[Session, Depends(get_database_session)],
                order_id: int):
    try:
        return reformat_order(db, order_crud.close_order(db, order_id))
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))
 

@router.get('/applications',
            responses={
                400: {'model': Message},
                401: {'model': Message},
                },
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def get_applications(db: Annotated[Session, Depends(get_database_session)]) -> list[ProductApplicationGet]:
     return reformat_applications(db, application_crud.get_all_applications(db))


@router.get('/applications/{application_id}',
            response_model=ProductApplicationGet,
            responses={
                400: {'model': Message},
                401: {'model': Message},
                404: {'model': Message},
                },
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def get_application_by_id(db: Annotated[Session, Depends(get_database_session)],
                           application_id: int):
    try:
        return reformat_app(db, application_crud.get_application(db, application_id))
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.post('/applications',
            response_model=ProductApplicationGet,
            responses={
                400: {'model': Message},
                401: {'model': Message},
                404: {'model': Message},
                },
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def create_new_application(db: Annotated[Session, Depends(get_database_session)],
                           application_part: ProductApplicationCreate):
    try:
        return reformat_app(db, application_crud.create_application(db, application_part))
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.delete('/applications/{application_id}',
            response_model=ProductApplicationGet,
            responses={
                400: {'model': Message},
                401: {'model': Message},
                404: {'model': Message},
                },
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def close_application(db: Annotated[Session, Depends(get_database_session)],
                           application_id: int):
    try:
        return reformat_app(db, application_crud.close_application(db, application_id))
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))

