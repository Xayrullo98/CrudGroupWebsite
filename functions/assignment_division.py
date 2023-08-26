from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.users import one_user, update_user, update_user_salary
from models.assignment_division import Assignment_division
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination
import datetime


def all_assignment_divisions(search, status, order_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Assignment_division.programmer_title.like(
            search_formatted) | Assignment_division.programmer_type.like(search_formatted)
    else:
        search_filter = Assignment_division.id > 0

    if status in [True, False]:
        status_filter = Assignment_division.status == status
    else:
        status_filter = Assignment_division.status.in_([True, False])

    if order_id:
        source_id_filter = Assignment_division.order_id == order_id
    else:
        source_id_filter = Assignment_division.order_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    assignment_divisions = db.query(Assignment_division).options(
        joinedload(Assignment_division.worker),joinedload(Assignment_division.order)).filter(search_filter, status_filter, source_id_filter).filter(
        Assignment_division.date_time > start_date).filter(
        Assignment_division.date_time <= end_date).order_by(Assignment_division.id.desc())
    if page and limit:
        return pagination(assignment_divisions, page, limit)
    else:
        return assignment_divisions.all()


def one_assignment_division(id, db):
    return db.query(Assignment_division).options(
        joinedload(Assignment_division.worker),joinedload(Assignment_division.order)).filter(Assignment_division.id == id).first()


async def create_assignment_division(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_user(form.order_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id order mavjud emas")

    new_assignment_division_db = Assignment_division(
        order_id=form.order_id,
        programmer_type=form.programmer_type,
        programmer_title=form.programmer_title,
        worker_id=form.worker_id,
        work_price=form.work_price,
        currency=form.currency,
        deadline=form.deadline,
        user_id=cur_user.id,
    )
    db.add(new_assignment_division_db)
    db.commit()
    data = NotificationBase(
        money=form.work_price,
        worker_id=form.worker_id,
        user_id=cur_user.id,
        type="assignment_division"
    )
    await manager.send_user(message=data, user_id=form.worker_id, db=db, )

    return new_assignment_division_db


async def update_assignment_division(form, cur_user, db):
    if one_assignment_division(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli assignment_division mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Assignment_division).filter(Assignment_division.id == form.id).update({
        Assignment_division.order_id: form.order_id,
        Assignment_division.programmer_type: form.programmer_type,
        Assignment_division.programmer_title: form.programmer_title,
        Assignment_division.worker_id: form.worker_id,
        Assignment_division.work_price: form.work_price,
        Assignment_division.currency: form.currency,
        Assignment_division.deadline: form.deadline,
        Assignment_division.user_id: cur_user.id,
        Assignment_division.status: form.status
    })
    db.commit()

    data = NotificationBase(
        money=form.money,
        worker_id=form.worker_id,
        user_id=cur_user.id,
        type="assignment_division"
    )
    await manager.send_user(message=data, user_id=form.worker_id, db=db, )
    return one_assignment_division(form.id, db)


def assignment_division_delete(id, cur_user, db):
    if one_assignment_division(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Assignment_division).filter(Assignment_division.id == id).update({
        Assignment_division.status: False,
        Assignment_division.user_id: cur_user.id
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}
