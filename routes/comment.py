
from fastapi import APIRouter, Depends, HTTPException
from db import Base, engine,get_db
import datetime
from sqlalchemy.orm import Session

from routes.auth import get_current_active_user

Base.metadata.create_all(bind=engine)


from functions.comment import one_comment, all_comments, create_comment, update_comment
from schemas.comment import *
from schemas.users import UserCurrent
router_comment = APIRouter()



@router_comment.post('/add', )
async def add_comment(form: CommentCreate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) : #current_user: CustomerBase = Depends(get_current_active_user)
    if await create_comment(form,current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")


@router_comment.get('/',  status_code = 200)
def get_comment(search: str = None, status: bool = True, id: int = 0,customer_id:int = 0, start_date=datetime.datetime.min.date(),end_date=datetime.datetime.max.date(),page: int = 1, limit: int = 25,
                db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user) ) : # current_user: User = Depends(get_current_active_user)
    if id :
        return one_comment(id, db)
    else :
        return all_comments(search=search,status=status,customer_id=customer_id, page=page, limit=limit,
                           db=db,start_date=start_date,end_date=end_date)


@router_comment.put("/update")
def comment_update(form: CommentUpdate, db: Session = Depends(get_db),current_user: UserCurrent = Depends(get_current_active_user)) :
    if update_comment(form, current_user, db) :
        raise HTTPException(status_code = 200, detail = "Amaliyot muvaffaqiyatli amalga oshirildi")



