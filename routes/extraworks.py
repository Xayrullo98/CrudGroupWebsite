from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.extraworks import one_extrawork, all_extraworks, create_extrawork, update_extrawork, extrawork_delete,select_extrawork
from schemas.extraworks import *
from schemas.users import UserCurrent

router_extrawork = APIRouter()


@router_extrawork.post('/add', )
def add_extrawork(form: ExtraWorksCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
    if create_extrawork(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_extrawork.get('/', status_code=200)
def get_extraworks(search: str = None, status: bool = True, id: int = 0,user_id:int=0,start_date=None, end_date = None, page: int = 1, limit: int = 25,
              db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return one_extrawork(id, db)
    else:
        return all_extraworks(search=search, status=status, page=page, limit=limit, db=db,user_id=user_id,start_date=start_date,end_date=end_date )


@router_extrawork.get('/user', status_code=200)
def get_extraworks(  page: int = 1, limit: int = 25, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):

    return select_extrawork(current_user,page,limit, db)


@router_extrawork.put("/update")
def extrawork_update(form: ExtraWorksUpdate, db: Session = Depends(get_db),
                current_user: ExtraWorksBase = Depends(get_current_active_user)):
    if update_extrawork(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_extrawork.delete('/{id}', status_code=200)
def delete_extrawork(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return extrawork_delete(id, current_user, db)
