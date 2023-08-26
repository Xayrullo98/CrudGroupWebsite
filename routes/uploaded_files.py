from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.uploaded_files import one_uploaded_files, all_uploaded_filess, create_uploaded_file, update_uploaded_files
from schemas.uploaded_files import UploadFile, UploadBase, UploadCreate,UploadUpdate
from schemas.users import UserCurrent

router_file=APIRouter()


@router_file.post('/add', )
def add_trade(form: UploadCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
	if create_uploaded_file(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_file.get('/', status_code=200)
def get_uploaded_files(search: str = None, status: bool = True, id: int = 0, order_id: int = 0,source_id: int = 0,source:str=None,start_date=None, end_date=None, page: int = 1, limit: int = 25,
               db: Session = Depends(get_db), current_user: UserCurrent = Depends(
		get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return one_uploaded_files(id, db)
	
	else:
		return all_uploaded_filess(search=search, status=status, order_id=order_id,source_id=source_id,start_date=start_date, end_date=end_date, page=page, limit=limit, db=db ,source=source)


@router_file.put("/update")
def trade_update(form: UploadUpdate, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(get_current_active_user)):
	if update_uploaded_files(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")



