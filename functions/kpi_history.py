import datetime
from time import sleep

from fastapi import HTTPException, WebSocket

from functions.kpi import filter_kpi
from functions import orders

from functions.trades import one_trade, get_order_id_from_trades, one_trade_via_order_id
from functions.users import one_user, update_user_salary, filter_users, update_user_balance
from models.incomes import Incomes
from models.kpi_history import Kpi_History

from models.extra import Extra
from models.orders import Orders
from models.trades import Trades
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_history(search, status, source_id, start_date, end_date, user_id, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Kpi_History.money.like(search_formatted) | Kpi_History.order_id.like(
            search_formatted)
    else:
        search_filter = Kpi_History.id > 0
    if status in [True, False]:
        status_filter = Kpi_History.status == status
    else:
        status_filter = Kpi_History.status.in_([True, False])

    if source_id:
        source_id_filter = Kpi_History.order_id == source_id
    else:
        source_id_filter = Kpi_History.id > 0
    if user_id:
        user_id_filter = Kpi_History.user_id == user_id
    else:
        user_id_filter = Kpi_History.id > 0
    try:
        if not start_date:
            start_date = datetime.date.min
        if not end_date:
            end_date = datetime.date.today()
        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
    history = db.query(Kpi_History).filter(Kpi_History.date > start_date).filter(
        Kpi_History.date <= end_date).filter(search_filter, status_filter, source_id_filter,
                                             user_id_filter).order_by(
        Kpi_History.id.desc())

    if page and limit:
        return pagination(history, page, limit)
    else:
        return history.all()


def filter_history_via_order_id(order_id, db):
    return db.query(Kpi_History).filter(Kpi_History.order_id == order_id).all()


def one_history(id, db):
    return db.query(Kpi_History).filter(Kpi_History.id == id).first()


def get_historys_via_order_id(order_id, db):
    return db.query(Kpi_History).filter(Kpi_History.order_id == order_id).all()


def all_payments(user_id, page, limit, db):
    history = db.query(Kpi_History).filter(Kpi_History.user_id == user_id).all()
    extra = db.query(Extra).filter(Extra.source_id == user_id).all()
    history = history + extra
    if page and limit:
        return pagination(history, page, limit)
    else:
        return history


async def create_history(form, cur_user, db):
    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

    if orders.one_order(form.order_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
    order = orders.one_order(id=form.order_id, db=db)
    if form.discount:
        updateorder_discount = db.query(Orders).filter(Orders.id == form.order_id).update({
            Orders.discount: form.discount
        })
        db.commit()

    # update user salary section
    user_kpi = filter_kpi(source_id=cur_user.id, db=db)
    get_order = orders.one_order(id=form.order_id, db=db)
    if not user_kpi:
        raise HTTPException(status_code=400, detail="Sizga kpi yaratilmagan")

    money = user_kpi.percentage * form.money / 100
    user = one_user(id=cur_user.id, db=db)
    real_money = get_order_id_from_trades(id=form.order_id, user=cur_user.id, db=db).get('money')
    money_real = get_order_id_from_trades(id=form.order_id, user=cur_user.id, db=db).get('real_money')
    rest_summ = real_money - form.money
    if real_money < form.money:
        raise HTTPException(status_code=400,
                            detail=f"Ortiqcha  {-1 * rest_summ} ming so'm to'lov qilinmoqda qayta kiriting")
    if int(real_money) == int(form.money):

        db.query(Orders).filter(Orders.id == form.order_id).update({
            Orders.id: form.order_id,
            Orders.user_id: user.id,
            Orders.order_status: 'design',
            Orders.design_date: datetime.datetime.now().date()

        })
        db.commit()

    else:
        db.query(Orders).filter(Orders.id == form.order_id).update({
            Orders.id: form.order_id,
            Orders.user_id: user.id,
            Orders.order_status: 'payment',

        })
        db.commit()

    # orders.update_summ ( id=form.order_id, summ=real_money, rest_summ=rest_summ, db=db )
    # orders.update_real_summ ( id=form.order_id, summ=money_real, db=db )
    # orders.update_payment ( id=form.order_id, money=form.money, db=db )
    # updated_salary=user.salary + money
    # update_user_salary ( id=cur_user.id, salary=updated_salary, db=db )
    # # user balance section
    # nasiya=real_money - form.money
    # money_balance=user_kpi.percentage * nasiya / 100
    # updated_balance=user.balance + money_balance
    # update_user_balance ( id=cur_user.id, balance=updated_balance, db=db )
    #
    # data=NotificationBase (
    #     money=money,
    #     worker_id=user.id,
    #     order_id=form.order_id,
    #     savdo_id=get_order.savdo_id,
    #     user_id=cur_user.id,
    #     name=user.name,
    #     type="trade"
    #
    # )
    # await manager.send_user ( message=data, user_id=user.id, db=db )
    #
    # new_history_db=Kpi_History (
    #     money=money,
    #     type=form.type,
    #     order_id=form.order_id,
    #     comment=form.comment,
    #     user_id=cur_user.id )
    # db.add ( new_history_db )
    # db.commit ( )

    new_income_db = Incomes(
        money=form.money,
        type=form.type,
        source_id=form.order_id,
        user_id=cur_user.id
    )
    db.add(new_income_db)
    db.commit()

    return new_income_db


def update_history(form, cur_user, db):
    if one_history(form.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo tarixi mavjud emas")

    if one_user(cur_user.id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")

    if one_trade(form.order_id, db) is None:
        raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

    db.query(Kpi_History).filter(Kpi_History.id == form.id).update({
        Kpi_History.money: form.money,
        Kpi_History.type: form.type,
        Kpi_History.order_id: form.order_id,
        Kpi_History.status: form.status,
        Kpi_History.comment: form.comment,
        Kpi_History.user_id: cur_user.id
    })
    db.commit()
    return one_history(form.id, db)


def update_history_status(order_id, user_id, db):
    if orders.one_order(order_id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")
    if one_user(user_id, db) is None:
        raise HTTPException(status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas")

    db.query(Kpi_History).filter(Kpi_History.order_id == order_id).update({
        Kpi_History.status: False,

    })
    db.commit()
    return one_history(order_id, db)
