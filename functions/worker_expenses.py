from fastapi import HTTPException
import datetime

from sqlalchemy.orm import joinedload


from functions.trades import one_trade
from functions.users import one_user, update_user_salary, update_user_company_balanse, filter_users
from models.users import Users
from models.worker_expenses import Worker_expenses
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_expenses(search, status, user_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Worker_expenses.money.like(search_formatted)
    else:
        search_filter = Worker_expenses.id > 0
    if status in [True, False]:
        status_filter = Worker_expenses.status == status
    else:
        status_filter = Worker_expenses.status.in_([True, False])

    if user_id:
        source_id_filter = Worker_expenses.user_id == user_id
    else:
        source_id_filter = Worker_expenses.id > 0

    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

    worker_expenses = db.query(Worker_expenses).options(joinedload(Worker_expenses.user).load_only(Users.name,Users.username,Users.number,Users.roll,)).filter(Worker_expenses.date_time > start_date).filter(
        Worker_expenses.date_time <= end_date).filter(search_filter, status_filter, source_id_filter).order_by(
        Worker_expenses.id.desc())
    if page and limit:
        return pagination(worker_expenses, page, limit)
    else:
        return worker_expenses.all()


def one_expense(id, db):
    return db.query(Worker_expenses).filter(Worker_expenses.id == id).first()


async def create_expense(money,type, cur_user, db,comment=''):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")


    user = one_user(id=cur_user.id, db=db)
    admin = filter_users(roll='admin',db=db)[0]
    if not  admin:
        admin={"id":1}
    updated_comp_balance = user.company_balance - money
    update_user_company_balanse(id=user.id, company_balance=updated_comp_balance, db=db)
    data = NotificationBase(
        money=money,
        name=user.name,
        worker_id=user.id,
        user_id=admin.id,
        type='worker_expense'
    )
    await manager.send_user(message=data, user_id=user.id, db=db)
    await manager.send_user(message=data, user_id=admin.id, db=db)
    new_expense_db = Worker_expenses(
        money=money,
        type=type,
        comment=comment,
        user_id=cur_user.id,

    )
    db.add(new_expense_db)
    db.commit()

    return new_expense_db


async def update_expense(form, cur_user, db):
    if one_expense(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
    worker = one_expense(id=form.id,db=db)
    if worker.money>form.money:
        user = one_user(id=cur_user.id, db=db)
        delta_money = worker.money-form.money
        updated_comp_balance = user.company_balance + delta_money
        update_user_company_balanse(id=user.id, company_balance=updated_comp_balance, db=db)
    else:
        user = one_user(id=cur_user.id, db=db)
        delta_money = form.money - worker.money
        updated_comp_balance = user.company_balance - delta_money
        update_user_company_balanse(id=user.id, company_balance=updated_comp_balance, db=db)
    data = NotificationBase(
            money=form.money,
            worker_id=user.id,
            user_id=cur_user.id,
            type='worker_expense'
        )
    await manager.send_user(message=data, user_id=user.id, db=db)
    db.query(Worker_expenses).filter(Worker_expenses.id == form.id).update({
        Worker_expenses.money: form.money,
        Worker_expenses.type: form.type,
        Worker_expenses.comment: form.comment,
        Worker_expenses.status: form.status
    })
    db.commit()
    return one_expense(form.id, db)


def expense_delete(id, db):
    if one_expense(id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")
    db.query(Worker_expenses).filter(Worker_expenses.id == id).update({
        Worker_expenses.status: False,
    })
    db.commit()
    return {"date": "Ma'lumot o'chirildi !"}