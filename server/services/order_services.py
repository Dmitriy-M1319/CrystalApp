from ..crud import product_crud


def reformat_orders_from_db(db, orders):
    result = []
    for order in orders:
        order_products = [
                {
                    'product': product_crud.get_product(db, prod.product_id), 
                    'count': prod.product_count
                    } for prod in order.orders_products]
        order_result = order.__dict__
        order_result['orders_products'] = order_products
        result.append(order_result)
    return result
