from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.done import one_done,all_dones,create_done,update_done,done_delete
from schemas.done import *
from schemas.users import UserCurrent

router_done=APIRouter()


@router_done.post('/add', )
async def add_done(form: DoneCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
	if await create_done(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_done.get('/', status_code=200)
def get_dones(search: str = None, status: bool = True,worker_id:int=0,start_date=None, end_date = None, id: int = 0, page: int = 1, limit: int = 25,
             db: Session = Depends(get_db), current_user: UserCurrent = Depends(get_current_active_user)):
	if id:
		return one_done(id, db)
	else:
		return all_dones(search=search, status=status, page=page, limit=limit, db=db,start_date=start_date,end_date=end_date,worker_id=worker_id )


@router_done.put("/update")
def done_update(form: DoneUpdate, db: Session = Depends(get_db),
               current_user: DoneBase = Depends(get_current_active_user)):
	if update_done(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_done.delete('/{id}', status_code=200)
def delete_done(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return done_delete(id, current_user, db)


