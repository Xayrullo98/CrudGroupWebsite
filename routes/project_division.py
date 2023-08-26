
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
import datetime
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.project_division import one_project_division, all_project_divisions, create_project_division, update_project_division
from schemas.project_division import *
from schemas.users import UserCurrent
router_project_division = APIRouter()



@router_project_division.post('/add', )
async def add_project_division(form: Project_divisionCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_project_division(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_project_division.get('/',  status_code = 200)
def get_project_division(search: str = None, status: bool = True, id: int = 0,worker_id:int = 0, start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_project_division(id, db)
    else :
        return all_project_divisions(search=search,status=status,worker_id=worker_id, page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_project_division.put("/update")
def project_division_update(form: Project_divisionUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_project_division(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



