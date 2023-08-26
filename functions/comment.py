from fastapi import HTTPException
from sqlalchemy.orm import Session

from functions.users import one_user, update_user, update_user_salary
from models.comment import Comment
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination
import datetime


def all_comments(search, status, customer_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Comment.text.like(search_formatted)
    else:
        search_filter = Comment.id > 0

    if status in [True, False]:
        status_filter = Comment.status == status
    else:
        status_filter = Comment.status.in_([True, False])

    if customer_id:
        source_id_filter = Comment.customer_id == customer_id
    else:
        source_id_filter = Comment.customer_id > 0

    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date()
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    comments = db.query(Comment).filter(search_filter, status_filter, source_id_filter).filter(
        Comment.date_time > start_date).filter(
        Comment.date_time <= end_date).order_by(Comment.id.desc())
    if page and limit:
        return pagination(comments, page, limit)
    else:
        return comments.all()


def one_comment(id, db):
    return db.query(Comment).filter(Comment.id == id).first()


async def create_comment(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if one_user(form.customer_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    new_comment_db = Comment(
        customer_id=form.customer_id,
        customer_monitoring_id=form.customer_monitoring_id,
        text=form.text,
        user_id=cur_user.id,
         )
    db.add(new_comment_db)
    db.commit()

    return new_comment_db


async def update_comment(form, cur_user, db):
    if one_comment(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli comment mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    db.query(Comment).filter(Comment.id == form.id).update({
        Comment.customer_id: form.customer_id,
        Comment.customer_monitoring_id: form.customer_monitoring_id,
        Comment.text: form.text,
        Comment.user_id: cur_user.id,
        Comment.status: form.status
    })
    db.commit()
    return one_comment(form.id, db)


def comment_delete(id, cur_user, db):
    if one_comment(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
    db.query(Comment).filter(Comment.id == id).update({
        Comment.status: False,
        Comment.user_id: cur_user.id
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}