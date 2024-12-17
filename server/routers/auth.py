from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from dependencies import check_permissions, get_database_session, get_token_from_header
from auth.dependencies import *
from schemas import user_schemas, extra_schemas
from crud import user_crud
from exceptions import RowNotFoundException


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@router.post('/register',
             response_model=user_schemas.UserModel,
             responses={400: {'model': extra_schemas.Message}})
def register_new_user(db: Annotated[Session, Depends(get_database_session)],
                      user: Annotated[user_schemas.UserCreate, Depends(hash_user_password)]):
    '''Зарегистрироваться новому пользователю в системе'''
    try:
        new_user = user_crud.create_user(db, user)
        return new_user
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))


@router.post('/reset_password',
             dependencies=[Depends(check_permissions)],
             response_model=extra_schemas.Success,
             responses={
                 400: {'model': extra_schemas.Message},
                 401: {'model': extra_schemas.Message},
                 404: {'model': extra_schemas.Message},
             })
def reset_password(db: Annotated[Session, Depends(get_database_session)],
                   token: Annotated[str, Depends(get_token_from_header)],
                   user_data: auth_schemas.PasswordUpdate):
    '''Сбросить пароль и поменять его на новый зарегистрированному пользователю'''
    try:
        reset_user_password(db, token, user_data)
        return {'success': True}
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
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
    '''Авторизоваться в приложении (получить JWT-токен для авторизации пользователя при выполнении действий)'''
    try:
        authenticated_user = authenticate(db, user)
        new_token = generate_token({'sub': authenticated_user.email})
        return {'access_token': new_token}
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.__str__)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))

