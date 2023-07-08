from fastapi import FastAPI

from .routers import products, users
from .db_engine import engine
from .models import user, application, order, product


user.Base.metadata.create_all(bind=engine)
application.Base.metadata.create_all(bind=engine)
order.Base.metadata.create_all(bind=engine)
product.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(products.router)
app.include_router(users.router)


@app.get('/')
async def index():
    return {'success': True}


