from sqlalchemy.orm import Session

from ..exceptions import RowNotFoundException
from ..schemas.cart_schemas import ProductCart
from ..models.order import Order, OrderProduct
from ..models.user import User
from ..schemas.order_schemas import *


def get_orders_by_client(client: User):
    return client.orders


def get_all_orders(database: Session):
    return database.query(Order).all()

def get_active_orders_for_client(client: User):
    return client.orders.filter(Order.order_status.is_(True)).all()


def _get_order_by_id(database: Session, order_id: int) -> Order:
    order = database.query(Order).filter(Order.id == order_id).one()
    if order is None:
        raise RowNotFoundException('Order', str(order_id))
    return order


def get_closed_orders_for_client(client: User):
    return get_orders_by_client(client).filter(Order.order_status.is_(False)).all()


def create_order(database: Session, 
                 cart: ProductCart,
                 client: User,
                 order_part: OrderCreate) -> Order:
    if len(cart.products) == 0:
        raise Exception('Cart is empty')
    new_order = Order(**order_part.dict())
    new_order.total_price = cart.all_sum 
    new_order.client = client
    database.add(new_order)
    database.commit()
    database.refresh(new_order)

    for product_count in cart.products:
        new_order_product = OrderProduct(order_id=new_order.id, 
                                         product_id=product_count[0].id,
                                         product_count=product_count[1])
        database.add(new_order_product)
        database.commit()

    return new_order


def close_order(database: Session,
                order_id: int) -> Order:
    order = _get_order_by_id(database, order_id)
    order.order_status = False
    database.commit()
    return order
