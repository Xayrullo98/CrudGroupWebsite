from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine, get_db

from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)

from functions.todo import one_todo,all_todos,create_todo,update_todo,todo_delete
from schemas.todo import *
from schemas.users import UserCurrent

router_todo=APIRouter()


@router_todo.post('/add', )
def add_todo(form: TodoCreate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: CustomerBase = Depends(get_current_active_user)
	if create_todo(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_todo.get('/', status_code=200)
def get_todos(search: str = None, status: bool = True, id: int = 0,user_id:int=0,start_date=None, end_date = None, page: int = 1, limit: int = 25,
             db: Session = Depends(get_db), current_user: UserCurrent = Depends(
		get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return one_todo(id, db)
	else:
		return all_todos(search=search, status=status,user_id=user_id, page=page, limit=limit, db=db,start_date=start_date,end_date=end_date )


@router_todo.put("/update")
def todo_update(form: TodoUpdate, db: Session = Depends(get_db),
               current_user: TodoBase = Depends(get_current_active_user)):
	if update_todo(form, current_user, db):
		raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_todo.delete('/{id}', status_code=200)
def delete_todo(id: int = 0, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
	get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
	if id:
		return todo_delete(id, current_user, db)


