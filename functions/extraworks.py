import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.users import one_user
from models.extraworks import ExtraWorks
from models.todo import Todo
from models.users import Users

from utils.pagination import pagination


def all_extraworks(search, status,user_id,start_date,end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = ExtraWorks.work.like(search_formatted)
    else:
        search_filter = ExtraWorks.id > 0
    if status in [True, False]:
        status_filter = ExtraWorks.status == status
    else:
        status_filter = ExtraWorks.status.in_([True, False])

    if user_id:
        user_filter = ExtraWorks.user_id==user_id
    else:
        user_filter = ExtraWorks.user_id>0

    try:
        if not start_date:
            start_date = datetime.date.min


        if not  end_date :
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    extrawork = db.query(ExtraWorks).options(
		joinedload(ExtraWorks.user).load_only(Users.name,Users.username)).filter(ExtraWorks.date > start_date).filter(
        ExtraWorks.date <= end_date).filter(search_filter, status_filter,user_filter,).order_by(ExtraWorks.id.desc())

    if page and limit:
        return pagination(extrawork, page, limit)
    else:
        return extrawork.all()


def one_extrawork(id, db):
    return db.query(ExtraWorks).options(
		joinedload(ExtraWorks.user).load_only(Users.name,Users.username)).filter(ExtraWorks.id == id).first()

def select_extrawork(user,page,limit, db):
    extrawork = db.query(ExtraWorks).options(
		joinedload(ExtraWorks.user).load_only(Users.name,Users.username)).filter(ExtraWorks.user_id == user.id)
    if page and limit:
        return pagination(extrawork, page, limit)
    else:
        return extrawork.all()


def create_extrawork(form, user, db):
    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    new_extrawork_db = ExtraWorks(
        work=form.work,
        user_id=user.id,

    )
    db.add(new_extrawork_db)
    db.commit()
    db.refresh(new_extrawork_db)
    return new_extrawork_db


def update_extrawork(form, user, db):
    if one_extrawork(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli extrawork mavjud emas")

    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(ExtraWorks).filter(ExtraWorks.id == form.id).update({
        ExtraWorks.id: form.id,
        ExtraWorks.status: form.status,
        ExtraWorks.work: form.work,
        ExtraWorks.user_id: user.id
    })
    db.commit()
    return one_extrawork(form.id, db)


def extrawork_delete(id, cur_user, db):
    if one_extrawork(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(ExtraWorks).filter(ExtraWorks.id == id).update({
        ExtraWorks.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
