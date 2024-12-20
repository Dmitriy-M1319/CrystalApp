from enum import Enum
import os
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from services.order_services import reformat_orders_from_db
from schemas.cart_schemas import ProductCart
from schemas.order_schemas import *
from schemas.extra_schemas import *
from crud import order_crud
from auth.dependencies import *
from dependencies import *
from services.report_services import get_report_by_period
from session.sessions import *


router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


class OrdersFilter(str, Enum):
    orders_all = 'all'
    orders_active = 'active'
    orders_closed = 'closed'


@router.get('/',
            responses={400: {'model': Message}})
def get_filtered_orders(db: Annotated[Session, Depends(get_database_session)],
                                   token: Annotated[str, Depends(get_token_from_header)],
                                   ord_filter: Annotated[OrdersFilter, Query(description='Фильтр для выборки')]) -> list[OrderGetForClient]:
    '''Получить заказы пользователя с возможной фильтрацией (все, активные, завершенные)'''
    try:
        curr_user = get_current_user(db, token)
        result = []
        match ord_filter:
            case OrdersFilter.orders_all:
                result = order_crud.get_orders_by_client(curr_user)
            case OrdersFilter.orders_active:
                result = order_crud.get_active_orders_for_client(curr_user)
            case OrdersFilter.orders_closed:
                result = order_crud.get_closed_orders_for_client(curr_user)
        return reformat_orders_from_db(db, result)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.post('/',
             responses={400: {'model': Message}},
             dependencies=[Depends(cookie)])
def create_order(db: Annotated[Session, Depends(get_database_session)],
                 token: Annotated[str, Depends(get_token_from_header)],
                 cart: Annotated[ProductCart, Depends(verifier)],
                 order_data: OrderCreate):
    '''Создать новый заказ для пользователя на основе его корзины'''
    try:
        curr_user = get_current_user(db, token)
        return order_crud.create_order(db, cart, curr_user, order_data)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post('/report',
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
            responses={
                200: {
                    "content": {"application/octet-stream": {}},
                    "description": "Return a xlsx report file",
                },
                400: {'model': Message},
                500: {'model': Message},
            })
def get_report(report_dates: GetOrdersReport):
    '''Получить отчет по продажам за определенный промежуток времени в формате Excel-таблицы'''
    code, msg, file_data = get_report_by_period(date_from=report_dates.from_date, date_to=report_dates.to_date)
    if(code != 200):
        raise HTTPException(status_code=code, detail=msg)
    else:
        if not os.path.exists(get_settings().reports_storage):
            os.mkdir(get_settings().reports_storage)
        filename = get_settings().reports_storage + f'/Report_{report_dates.from_date}_{report_dates.to_date}.xlsx'
        with open(filename, "wb") as file:
            file.write(file_data)
        return FileResponse(path=filename, filename=filename, media_type='multipart/form-data')
        

