#TODO: Навесить обработку исключений
#TODO: Проверить, почему не показываются продукты в order_products
from enum import Enum
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..schemas.cart_schemas import ProductCart
from ..schemas.order_schemas import *
from ..schemas.extra_schemas import *
from ..crud import order_crud
from ..auth.dependencies import *
from ..dependencies import *
from ..session.sessions import *


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
                                   ord_filter: Annotated[OrdersFilter, Query()]):
    try:
        curr_user = get_current_user(db, token)
        match ord_filter:
            case OrdersFilter.orders_all:
                if curr_user.is_admin:
                    return order_crud.get_all_orders(db)
                else:
                    return order_crud.get_orders_by_client(curr_user)
            case OrdersFilter.orders_active:
                return order_crud.get_active_orders_for_client(curr_user)
            case OrdersFilter.orders_closed:
                return order_crud.get_closed_orders_for_client(curr_user)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))


@router.post('/',
             dependencies=[Depends(cookie)])
def create_order(db: Annotated[Session, Depends(get_database_session)],
                 token: Annotated[str, Depends(get_token_from_header)],
                 cart: Annotated[ProductCart, Depends(verifier)],
                 order_data: OrderCreate):
    try:
        curr_user = get_current_user(db, token)
        return order_crud.create_order(db, cart, curr_user, order_data)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/{order_id}',
               response_model=OrderGetForAdmin,
               dependencies=[Depends(check_permissions), Depends(check_admin_permissions)])
def close_order(db: Annotated[Session, Depends(get_database_session)],
                order_id: int):
    try:
        return order_crud.close_order(db, order_id)
    except SQLAlchemyError as sql_error:
        raise HTTPException(status_code=400, detail=str(sql_error.__dict__['orig']))
    

