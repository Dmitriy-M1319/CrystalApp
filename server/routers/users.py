#TODO: Сделать валидацию на все ключи и некоторые поля

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import RowNotFoundException
from ..dependencies import *
from ..schemas import user_schemas, extra_schemas
from ..crud import user_crud


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/me',
            response_model=user_schemas.UserModel,
            responses={
                404: {'model': extra_schemas.Message},
                400: {'model': extra_schemas.Message}
            })
def get_authenticated_user(db: Annotated[Session, Depends(get_database_session)],
                           token: Annotated[str, Depends(get_token_from_header)]):
    return get_current_user(db, token)


@router.get('/{user_id}',
            response_model=user_schemas.UserModel,
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
            responses={404: {'model': extra_schemas.Message}})
def get_user_by_id(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    try:
        return user_crud.get_user(db, user_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)


@router.get('/{email}',
            response_model=user_schemas.UserModel,
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
            responses={404: {'model': extra_schemas.Message}})
def get_user_by_email(db: Annotated[Session, Depends(get_database_session)], email: str):
    try:
        return user_crud.get_user_by_email(db, email)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)


@router.put('/{user_id}',
            response_model=user_schemas.UserModel,
            dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
            responses={
                400: {'model': extra_schemas.Message},
                404: {'model': extra_schemas.Message}})
def update_user(db: Annotated[Session, Depends(get_database_session)],
                user_id: int, user: user_schemas.UserUpdate):
    try:
        return user_crud.update_user(db, user_id, user)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e.__dict__['orig']))


@router.delete('/{user_id}',
               response_model=user_schemas.UserModel,
               dependencies=[Depends(check_permissions), Depends(check_admin_permissions)],
               responses={404: {'model': extra_schemas.Message}})
def remove_user(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    try:
        return user_crud.delete_user(db, user_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
