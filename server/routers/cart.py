from fastapi import APIRouter, Response, Depends, Path
from pydantic import Field

from exceptions import RowNotFoundException
from dependencies import *
from schemas.cart_schemas import ProductCart
from session.sessions import *
from crud import cart_crud
from schemas.extra_schemas import *


router = APIRouter(
    prefix='/cart',
    tags=['cart']
)


class AddProduct(BaseModel):
    product_id: int = Field(gt=0)
    count_for_order: int = Field(gt=0)


@router.post('/',
             responses={401: {'model': Message}},
             dependencies=[Depends(check_permissions)])
async def create_session_cart(cart: ProductCart, response: Response):
    '''Создать новую корзину для пользователя'''
    return await cart_crud.create_session_cart(cart, response)


@router.get('/', response_model=ProductCart,
            responses={401: {'model': Message}},
            dependencies=[Depends(cookie), Depends(check_permissions)])
async def get_current_cart(cart: Annotated[ProductCart, Depends(verifier)]):
    '''Получить текущую корзину авторизованного пользователя'''
    return cart


@router.post('/add_product', 
             responses={401: {'model': Message},
                        404: {'model': Message},
                        400: {'model': Message}},
             dependencies=[Depends(cookie),Depends(check_permissions)])
async def add_product_to_cart(session_id: Annotated[UUID, Depends(cookie)], 
                              cart: Annotated[ProductCart, Depends(verifier)],
                              db: Annotated[Session, Depends(get_database_session)],
                              product: AddProduct):
    '''Добавить новый товар в определенном количестве в корзину'''
    try:
        return await cart_crud.add_product_to_cart(db, \
            cart, session_id, product.product_id, product.count_for_order)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete('/remove_product/{product_id}', response_model=ProductCart, 
               responses={401: {'model': Message},
                          404: {'model': Message}},
               dependencies=[Depends(cookie), Depends(check_permissions)])
async def remove_product_from_cart(product_id: Annotated[int, Path(ge=1, description='ID товара')], 
                              session_id: Annotated[UUID, Depends(cookie)],
                              cart: Annotated[ProductCart, Depends(verifier)]):
    '''Убрать полностью товар по его идентификатору из корзины пользователя'''
    try:
        return await cart_crud.remove_product_from_cart(cart, session_id, product_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/', 
               response_model=Success,
               responses={401: {'model': Message}},
               dependencies=[Depends(check_permissions)])
async def delete_session_cart(response: Response, session_id: Annotated[UUID, Depends(cookie)]):
    '''Удалить сессионную корзину пользователя'''
    await cart_crud.delete_session_cart(response, session_id)
    return {'success': True}
