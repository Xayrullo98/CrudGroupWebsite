
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
import datetime
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.customer_monitoring import one_customer_monitoring, all_customer_monitorings, create_customer_monitoring, update_customer_monitoring
from schemas.customer_monitoring import *
from schemas.users import UserCurrent
router_customer_monitoring = APIRouter()



@router_customer_monitoring.post('/add', )
async def add_customer_monitoring(form: Customer_monitoringCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_customer_monitoring(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_customer_monitoring.get('/',  status_code = 200)
def get_customer_monitoring(search: str = None, status: bool = True, id: int = 0,customer_id:int = 0, start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_customer_monitoring(id, db)
    else :
        return all_customer_monitorings(search=search,status=status,customer_id=customer_id, page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_customer_monitoring.put("/update")
def customer_monitoring_update(form: Customer_monitoringUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_customer_monitoring(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



