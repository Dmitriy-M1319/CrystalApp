from typing import Annotated

from fastapi import APIRouter, Response, Depends, Path
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..dependencies import *
from ..schemas.cart_schemas import ProductCart
from ..session.sessions import *
from ..crud import cart_crud
from ..schemas.extra_schemas import *

router = APIRouter(
    prefix='/cart',
    tags=['cart']
)

class AddProduct(BaseModel):
    product_id: int
    count_for_order: int


@router.post('/',
             response_model=Message,
             responses={401: {'model': Message}},
             dependencies=[Depends(check_permissions)])
async def create_session_cart(cart: ProductCart, response: Response):
   await cart_crud.create_session_cart(cart, response)
   return {'success': True}


@router.get('/', response_model=ProductCart,
            responses={401: {'model': Message}},
            dependencies=[Depends(cookie), Depends(check_permissions)])
async def get_current_cart(cart: Annotated[ProductCart, Depends(verifier)]):
    return cart


@router.post('/add_product', response_model=ProductCart, 
             responses={401: {'model': Message},
                        404: {'model': Message},
                        400: {'model': Message}},
             dependencies=[Depends(cookie),Depends(check_permissions)])
async def add_product_to_cart(session_id: Annotated[UUID, Depends(cookie)], 
                              cart: Annotated[ProductCart, Depends(verifier)],
                              db: Annotated[Session, Depends(get_database_session)],
                              product: AddProduct):
    return cart_crud.add_product_to_cart(db, cart, session_id, product.product_id, product.count_for_order)


@router.delete('/remove_product/{product_id}', response_model=ProductCart, 
               responses={401: {'model': Message},
                          404: {'model': Message}},
               dependencies=[Depends(cookie), Depends(check_permissions)])
async def remove_product_from_cart(product_id: Annotated[int, Path(ge=1)], 
                              session_id: Annotated[UUID, Depends(cookie)],
                              cart: Annotated[ProductCart, Depends(verifier)]):
    return cart_crud.remove_product_from_cart(cart, session_id, product_id)


@router.delete('/', 
               response_model=Message,
               responses={401: {'model': Message}},
               dependencies=[Depends(check_permissions)])
async def delete_session_cart(response: Response, session_id: Annotated[UUID, Depends(cookie)]):
    await cart_crud.delete_session_cart(response, session_id)
    return {'success': True}
