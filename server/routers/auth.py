from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import RowNotFoundException
from ..dependencies import get_database_session
from ..auth.dependencies import *
from ..schemas import auth_schemas, user_schemas, extra_schemas
from ..crud import user_crud


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register',
             response_model=user_schemas.UserModel,
             responses={400: {'model': extra_schemas.Message}})
def register_new_user(db: Annotated[Session, Depends(get_database_session)],
                      user: Annotated[user_schemas.UserCreate, Depends(hash_user_password)]):
    try:
        new_user = user_crud.create_user(db, user)
        return new_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))


@router.post('/token',
             response_model=auth_schemas.Token,
             responses={
                 400: {'model': extra_schemas.Message},
                 401: {'model': extra_schemas.Message},
                 404: {'model': extra_schemas.Message},
             })
def login_user_for_token(db: Annotated[Session, Depends(get_database_session)],
                         user: auth_schemas.AuthenticateUserData):
    try:
        authenticated_user = authenticate(db, user)
        new_token = generate_token({'sub': authenticated_user.email})
        return {'access_token': new_token}
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))
