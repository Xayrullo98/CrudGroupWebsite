
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
import datetime
from sqlalchemy.orm import Session
from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.assignment_division import one_assignment_division, all_assignment_divisions, create_assignment_division, update_assignment_division
from schemas.assignment_division import *
from schemas.users import UserCurrent
router_assignment_division = APIRouter()



@router_assignment_division.post('/add', )
async def add_assignment_division(form: AssignmentCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_assignment_division(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_assignment_division.get('/',  status_code = 200)
def get_assignment_division(search: str = None, status: bool = True, id: int = 0,order_id:int = 0,customer_id:int=0, start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_assignment_division(id, db)
    else :
        return all_assignment_divisions(search=search,status=status,order_id=order_id, page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_assignment_division.put("/update")
def assignment_division_update(form: AssignmentUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_assignment_division(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



