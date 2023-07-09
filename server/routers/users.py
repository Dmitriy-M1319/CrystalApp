from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..exceptions import RowNotFoundException
from ..dependencies import get_database_session
from ..schemas import user_schemas, extra_schemas
from ..crud import user_crud


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/{user_id}',
            response_model=user_schemas.UserModel,
            responses={404: {'model': extra_schemas.Message}})
def get_user(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    try:
        return user_crud.get_user(db, user_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)


@router.get('/{email}',
            response_model=user_schemas.UserModel,
            responses={404: {'model': extra_schemas.Message}})
def get_user(db: Annotated[Session, Depends(get_database_session)], email: str):
    try:
        return user_crud.get_user_by_email(db, email)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)


@router.put('/{user_id}',
            response_model=user_schemas.UserModel,
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
               responses={404: {'model': extra_schemas.Message}})
def remove_user(db: Annotated[Session, Depends(get_database_session)], user_id: int):
    try:
        return user_crud.delete_user(db, user_id)
    except RowNotFoundException as e:
        raise HTTPException(status_code=404, detail=e)
