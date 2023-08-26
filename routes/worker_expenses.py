import shutil
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from pydantic import typing

from db import Base, engine, get_db

from sqlalchemy.orm import Session

from functions.uploaded_files import create_uploaded_file
from functions.users import one_user, update_user_company_balanse
from models.worker_expenses import Worker_expenses
from routes.auth import get_current_active_user
from routes.notification import manager
from schemas.notification import NotificationBase

Base.metadata.create_all(bind=engine)

from functions.worker_expenses import one_expense, all_expenses, update_expense, create_expense, expense_delete
from schemas.worker_expenses import WorkerCreate, WorkerUpdate
from schemas.users import UserCurrent

router_expense = APIRouter()




@router_expense.post('/add', )
async def add_expense(money: float = Body(..., ge=0),
                      type: str = Body(''),
                      comment: typing.Optional[str] = Body(''),
                      files: typing.Optional[List[UploadFile]] = File(None), db: Session = Depends(get_db),
                      current_user: UserCurrent = Depends(get_current_active_user)):


    user = one_user(id=current_user.id, db=db)

    updated_comp_balance = user.company_balance - money
    update_user_company_balanse(id=user.id, company_balance=updated_comp_balance, db=db)
    data = NotificationBase(
        money=money,
        worker_id=user.id,
        user_id=current_user.id,
        type='worker_expense'
    )
    await manager.send_user(message=data, user_id=user.id, db=db)
    new_expense_db = Worker_expenses(
        money=money,
        type=type,
        comment=comment,
        user_id=current_user.id,

    )
    db.add(new_expense_db)
    db.commit()

    if files:
            for file in files:
                with open("media/" + file.filename, 'wb') as image:
                    shutil.copyfileobj(file.file, image)
                url = str('media/' + file.filename)
                create_uploaded_file(source_id=new_expense_db.id, source='company_balance', file_url=url, comment=comment,
                                     user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_expense.get('/', status_code=200)
def get_expenses(search: str = None, status: bool = True, id: int = 0, user_id: int = 0, start_date=None,
                 end_date=None, page: int = 1, limit: int = 25, db: Session = Depends(get_db),
                 current_user: UserCurrent = Depends(
                     get_current_active_user)):  # current_user: User = Depends(get_current_active_user)
    if id:
        return one_expense(id, db)
    else:
        return all_expenses(search, status, user_id, start_date, end_date, page, limit, db, )


@router_expense.put("/update")
async def expense_update(form: WorkerUpdate, db: Session = Depends(get_db),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    if await update_expense(form, current_user, db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@router_expense.delete('/{id}', status_code=200)
def delete_expense(id: int = 0, db: Session = Depends(get_db),
                   current_user: UserCurrent = Depends(get_current_active_user)):
    if id:
        return expense_delete(id, db)
