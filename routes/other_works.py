from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import Base, engine, get_db
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.other_works import one_other_work, all_other_works, create_other_work, update_other_work, \
	other_work_delete, select_other_work, other_work_result
from schemas.other_works import *
from schemas.users import UserCurrent

router_other_work=APIRouter()


@router_other_work.post('/add', )
async def add_other_work(form: OtherWorksCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
	if await create_other_work(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_other_work.get('/', status_code=200)
def get_other_works(search: str = None, status: bool = True, id: int = 0, user_id: int = 0, start_date=None,
                    end_date=None, result: bool = None, page: int = 1, limit: int = 25,
                    db: Session = Depends(get_db), current_user: UserCurrent = Depends(
		get_current_active_user)):
	if id:
		return one_other_work(id, db)
	else:
		return all_other_works(search=search, status=status, page=page, limit=limit, db=db, user_id=user_id,
		                       start_date=start_date, end_date=end_date, result=result)


@router_other_work.get('/user', status_code=200)
def get_other_works(page: int = 1, limit: int = 25, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):
	return select_other_work(current_user, page, limit, db)


@router_other_work.put('/result', )
async def get_other_works(id: int = 0, result: bool = None, db: Session = Depends(get_db),
                          current_user: UserCurrent = Depends(
	                          get_current_active_user)):
	return await other_work_result(id=id, result=result, db=db, cur_user=current_user)


@router_other_work.put("/update")
def other_work_update(form: OtherWorksUpdate, db: Session = Depends(get_db),
                      current_user: OtherWorksBase = Depends(get_current_active_user)):
	if update_other_work(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_other_work.delete('/{id}', status_code=200)
def delete_other_work(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return other_work_delete(id, current_user, db)



