from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from functions.orders import one_order
from functions.users import one_user, update_user, update_user_salary
from models.project_division import Project_division

from utils.pagination import pagination
import datetime


def all_project_divisions(search, status, worker_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Project_division.text.like(search_formatted)
    else:
        search_filter = Project_division.id > 0

    if status in [True, False]:
        status_filter = Project_division.status == status
    else:
        status_filter = Project_division.status.in_([True, False])

    if worker_id:
        source_id_filter = Project_division.worker_id == worker_id
    else:
        source_id_filter = Project_division.worker_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    project_divisions = db.query(Project_division).options(
        joinedload(Project_division.worker),joinedload(Project_division.order)).filter(search_filter, status_filter, source_id_filter).filter(
        Project_division.date_time > start_date).filter(
        Project_division.date_time <= end_date).order_by(Project_division.id.desc())
    if page and limit:
        return pagination(project_divisions, page, limit)
    else:
        return project_divisions.all()


def one_project_division(id, db):
    return db.query(Project_division).options(
        joinedload(Project_division.worker),joinedload(Project_division.order)).filter(Project_division.id == id).first()


async def create_project_division(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_user(form.worker_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id ishchi mavjud emas")
    if one_order(form.order_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id order mavjud emas")
    new_project_division_db = Project_division(
        order_id=form.order_id,
        worker_id=form.worker_id,
        text=form.text,
        deadline=form.deadline,
        user_id=cur_user.id,
    )
    db.add(new_project_division_db)
    db.commit()

    return new_project_division_db


async def update_project_division(form, cur_user, db):
    if one_project_division(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli project_division mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Project_division).filter(Project_division.id == form.id).update({
        Project_division.order_id: form.order_id,
        Project_division.worker_id: form.worker_id,
        Project_division.text: form.text,
        Project_division.user_id: cur_user.id,
        Project_division.deadline: form.deadline,
        Project_division.status: form.status
    })
    db.commit()
    return one_project_division(form.id, db)


def project_division_delete(id, cur_user, db):
    if one_project_division(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Project_division).filter(Project_division.id == id).update({
        Project_division.status: False,
        Project_division.user_id: cur_user.id
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}