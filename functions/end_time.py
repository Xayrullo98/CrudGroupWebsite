from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.users import one_user
from models.end_time import End_time
from models.users import Users
from utils.pagination import pagination


def all_end_times(search, status, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = End_time.date.like(search_formatted)

    else:
        search_filter = End_time.id > 0
    if status in [True, False]:
        status_filter = End_time.status == status
    else:
        status_filter = End_time.status.in_([True, False])

    end_times = db.query(End_time).filter(search_filter, status_filter).order_by(End_time.id.desc())


    return end_times.first()


def one_end_time(id, db):
    return db.query(End_time).filter(End_time.id == id).first()


def create_end_time(form, user, db):
    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")


    new_end_time_db = End_time(
        date=form.date,
        user_id=user.id,

    )
    db.add(new_end_time_db)
    db.commit()
    db.refresh(new_end_time_db)
    return new_end_time_db


def update_end_time(form, user, db):
    if one_end_time(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli end_time mavjud emas")

    if one_user(user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(End_time).filter(End_time.id == form.id).update({
        End_time.id: form.id,
        End_time.status: form.status,
        End_time.date: form.date,
        End_time.user_id: user.id
    })
    db.commit()
    return one_end_time(form.id, db)