from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.users import one_user, update_user, update_user_salary
from models.customer_monitoring import Customer_monitoring
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination
import datetime


def all_customer_monitorings(search, status, customer_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Customer_monitoring.programmer_title.like(search_formatted)|Customer_monitoring.programmer_type.like(search_formatted)
    else:
        search_filter = Customer_monitoring.id > 0

    if status in [True, False]:
        status_filter = Customer_monitoring.status == status
    else:
        status_filter = Customer_monitoring.status.in_([True, False])

    if customer_id:
        source_id_filter = Customer_monitoring.customer_id == customer_id
    else:
        source_id_filter = Customer_monitoring.customer_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    customer_monitorings = db.query(Customer_monitoring).options(
        joinedload(Customer_monitoring.customer),joinedload(Customer_monitoring.comment)).filter(search_filter, status_filter, source_id_filter).filter(
        Customer_monitoring.date_time > start_date).filter(
        Customer_monitoring.date_time <= end_date).order_by(Customer_monitoring.id.desc())
    if page and limit:
        return pagination(customer_monitorings, page, limit)
    else:
        return customer_monitorings.all()


def one_customer_monitoring(id, db):
    return db.query(Customer_monitoring).filter(Customer_monitoring.id == id).first()


async def create_customer_monitoring(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_user(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    new_customer_monitoring_db = Customer_monitoring(
        customer_id=form.customer_id,
        customer_status=form.customer_status,
        monitoring_status=form.monitoring_status,
        user_id=cur_user.id,
         )
    db.add(new_customer_monitoring_db)
    db.commit()

    return new_customer_monitoring_db


async def update_customer_monitoring(form, cur_user, db):
    if one_customer_monitoring(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli customer_monitoring mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Customer_monitoring).filter(Customer_monitoring.id == form.id).update({
        Customer_monitoring.customer_id: form.customer_id,
        Customer_monitoring.customer_status: form.customer_status,
        Customer_monitoring.user_id: cur_user.id,
        Customer_monitoring.status: form.status
    })
    db.commit()



    return one_customer_monitoring(form.id, db)


def customer_monitoring_delete(id, cur_user, db):
    if one_customer_monitoring(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Customer_monitoring).filter(Customer_monitoring.id == id).update({
        Customer_monitoring.status: False,
        Customer_monitoring.user_id: cur_user.id
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}