from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from routers import products, users, auth, cart, orders, admin
from db_engine import engine
from models import user, application, order, product


def custom_docs():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CrystalApp",
        version="0.1.0",
        summary="Документация OpenAPI для приложения CrystalApp",
        description="Данная документация предоставляет API для информационной системы, представляющей собой интернет-магазин для реализации фильтров для воды, а также менеджмент-систему склада и заказов пользователей для администраторов",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


user.Base.metadata.create_all(bind=engine)
application.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)

app.openapi = custom_docs




