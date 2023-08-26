from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.end_time import one_end_time, all_end_times, create_end_time, update_end_time
from schemas.end_time import *
from schemas.users import UserCurrent

router_end_time = APIRouter()


@router_end_time.post('/add', )
def add_time(form: End_time_Create, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
    if create_end_time(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_end_time.get('/', status_code=200)
def get_times(search: str = None, status: bool = True, id: int = 0, page: int = 1, limit: int = 25,
             db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    if id:
        return one_end_time(id, db)
    else:
        return all_end_times(search, status, page, limit, db, )


@router_end_time.put("/update")
def time_update(form: End_time_Update, db: Session = Depends(get_db),
               current_user: End_time_Base = Depends(get_current_active_user)):
    if update_end_time(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")





