from uuid import uuid4, UUID

from fastapi import Response
from sqlalchemy.orm import Session

from ..exceptions import RowNotFoundException
from ..schemas.product_schemas import ProductGetModel
from ..session.sessions import *
from ..schemas.cart_schemas import ProductCart
from .product_crud import get_product


async def create_session_cart(cart: ProductCart, response: Response):
    session_id = uuid4()
    await session_back.create(session_id, cart)
    cookie.attach_to_response(response, session_id)


async def add_product_to_cart(db: Session,
                              cart: ProductCart,
                              session_id: UUID,
                              product_id: int,
                              products_count: int = 1) -> ProductCart:
    product = ProductGetModel (**get_product(db, product_id).dict())
    if products_count > product.count_on_warehouse:
        raise Exception('Too many products in cart')
    cart.products[product] = products_count
    cart.all_sum += product.client_price * products_count
    await session_back.update(session_id, cart)
    return cart


async def remove_product_from_cart(cart: ProductCart,
                                   session_id: UUID,
                                   product_id: int) -> ProductCart:
    for product in cart.products.keys():
        if product.id == product_id:
            cart.all_sum -= product.client_price * cart.products[product]
            del cart.products[product]
            await session_back.update(session_id, cart)
            return cart

    else:
        raise RowNotFoundException('Product', str(product_id))


async def delete_session_cart(response: Response, session_id: UUID):
    await session_back.delete(session_id)
    cookie.delete_from_response(response)

