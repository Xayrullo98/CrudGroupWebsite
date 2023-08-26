
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
import datetime
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.incomes import one_income, all_incomes, create_income, update_income, result_of_incomes_and_expenses
from schemas.incomes import *
from schemas.users import UserCurrent
router_income = APIRouter()



@router_income.post('/add', )
async def add_income(form: IncomeCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_income(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_income.get('/',  status_code = 200)
def get_incomes(search: str = None, status: bool = True, id: int = 0,order_id:int = 0,customer_id:int=0, start_date=None,end_date=None,page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_income(id, db)
    else :
        return all_incomes(search=search,status=status,order_id=order_id,customer_id=customer_id, page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_income.put("/update")
def income_update(form: IncomeUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_income(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_income.get ( '/result', status_code=200 )
def get_orders_result(start_date=datetime.datetime.now().date().min, end_date=datetime.datetime.now().today().date(), today=None, db: Session = Depends ( get_db ),
                      current_user: UserCurrent = Depends (
            get_current_active_user )):
    return result_of_incomes_and_expenses(start_date=start_date,end_date=end_date,today=today,db=db)

