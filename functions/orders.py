from fastapi import HTTPException
from sqlalchemy import and_, cast, Date, func
from sqlalchemy.orm import joinedload, Session, join
from pydantic.datetime_parse import datetime, date
from sqlalchemy import or_
from db import SessionLocal
from functions.customers import one_customer
from functions.kpi_history import get_historys_via_order_id
from functions.uploaded_files import one_uploaded_file_via_source
from functions.users import one_user, update_user_salary

from models.customers import Customers
from models.incomes import Incomes
import datetime

from models.kpi_history import Kpi_History
from models.orders import Orders

from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_orders(search, status, userid, customerid, order_status, start_date, end_date, season_id, page, limit, db):
    if search:
        search_formatted="%{}%".format ( search )
        search_filter=Orders.comment.like ( search_formatted ) | Orders.savdo_id.like ( search_formatted )
    else:
        search_filter=Orders.id > 0
    if status in [True, False]:
        status_filter=Orders.status == status
    else:
        status_filter=Orders.status.in_ ( [True, False] )

    if userid:
        userfilter=Orders.user_id == userid
    else:
        userfilter=Orders.user_id > 0
    if customerid:
        customerfilter=Orders.customer_id == customerid
    else:
        customerfilter=Orders.customer_id > 0


    if order_status:
        order_filter_for_seller=Orders.order_status == order_status
    else:
        order_filter_for_seller=Orders.id > 0

    try:
        if not start_date:
            start_date=datetime.date.min
        if not end_date:
            end_date=datetime.date.today ( )
        end_date=datetime.datetime.strptime ( str ( end_date ), '%Y-%m-%d' ).date ( ) + datetime.timedelta ( days=1 )
    except Exception as error:
        raise HTTPException ( status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  " )
    orders=db.query ( Orders ).options (
        joinedload ( Orders.customer ),joinedload ( Orders.user )).filter (
        Orders.date > start_date ).filter (
        Orders.date <= end_date ).filter ( search_filter, userfilter, customerfilter, status_filter,
                                           order_filter_for_seller ).order_by ( Orders.id.desc ( ) )

    if page and limit:
        return pagination ( orders, page, limit )
    else:
        return orders.all ( )


def one_order(id, db):
    data=db.query ( Orders ).options (
        joinedload ( Orders.customer ), joinedload ( Orders.user )).filter ( Orders.id == id ).first ( )

    return data





def last_savdo(db):


    return db.query ( Orders ).order_by ( Orders.id.desc ( ) ).first ( )


def create_order(form, user, db):
    if one_user ( user.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas" )

    if one_customer ( form.customer_id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli mijoz mavjud emas" )



    savdo=last_savdo ( db )
    if savdo:
        savdo_id=savdo.savdo_id + 1
        new_order_db=Orders (
            customer_id=form.customer_id,
            comment=form.comment,
            user_id=user.id,
            savdo_id=savdo_id,
            deadline=form.deadline,
            created_date=datetime.datetime.now().date(),
            order_status='created'

        )
        db.add ( new_order_db )
        db.commit ( )
        db.refresh ( new_order_db )

        return {'data': new_order_db}

    else:
        savdo=1
        new_order_db=Orders (
            customer_id=form.customer_id,
            comment=form.comment,
            user_id=user.id,
            savdo_id=savdo,
            deadline=form.deadline,
            created_date=datetime.datetime.now ( ).date ( ),
            order_status='created'
        )
        db.add ( new_order_db )
        db.commit ( )
        db.refresh ( new_order_db )

        return {'data': new_order_db, }


def update_order(form, user, db):
    if one_order ( form.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli mahsulot mavjud emas" )

    if one_user ( user.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli user mavjud emas" )

    db.query ( Orders ).filter ( Orders.id == form.id ).update ( {
        Orders.id: form.id,
        Orders.customer_id: form.customer_id,
        Orders.status: form.status,
        Orders.comment: form.comment,
        Orders.user_id: user.id,
        Orders.deadline: form.deadline

    } )
    db.commit ( )
    return one_order ( form.id, db )


def nextlevelupdate(id, order_status, user, db):
    if one_order ( id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli mahsulot mavjud emas" )

    if one_user ( user.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli user mavjud emas" )

    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.id: id,
        Orders.user_id: user.id,
        Orders.order_status: order_status,
        Orders.updated_day: datetime.datetime.utcnow( ).date ( )

    } )
    db.commit ( )
    return one_order ( id, db )


def update_order_status(order_id, user_id, db):
    if one_order ( order_id, db ) is None:
        raise HTTPException ( status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas" )
    if one_user ( user_id, db ) is None:
        raise HTTPException ( status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas" )

    db.query ( Orders ).filter ( Orders.id == order_id ).update ( {
        Orders.status: False,

    } )
    db.commit ( )
    return one_order ( order_id, db )


def update_order_status_via_season_id(season_id, user_id, db):
    if one_user ( user_id, db ) is None:
        raise HTTPException ( status_code=400, detail=f"Bunday {user_id} raqamli user mavjud emas" )
    seasons=db.query ( Orders ).filter ( Orders.season_id == season_id ).all ( )

    for season in seasons:
        db.query ( Orders ).filter ( Orders.id == season.id ).update ( {
            Orders.status: False,

        } )
        db.commit ( )
    return {"date": "Ma'lumot o'chirildi !"}


def order_delete(id, user, db):
    if one_order ( id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas" )
    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.status: False,
        Orders.user_id: user.id
    } )
    db.commit ( )
    return {"date": "Ma'lumot o'chirildi !"}








def update_summ(id, summ, db, rest_summ=None):
    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.summ: summ,
        Orders.rest_summ: rest_summ} )

    db.commit ( )


def update_real_summ(id, summ, db, ):
    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.real_summ: summ,
    } )

    db.commit ( )


def update_payment(id, money, db, ):
    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.payment_summ: money,
    } )

    db.commit ( )


"""
db.query(Kpi_History).filter(Kpi_History.order_id == order_id).update({
        Kpi_History.status: False,

    })
"""


async def returned_products(id, user, db):
    if one_order ( id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli mahsulot mavjud emas" )
    order=one_order ( id=id, db=db )
    historys=get_historys_via_order_id ( order_id=order.id, db=db )

    for history in historys:
        user=one_user ( id=history.user_id, db=db )
        updated_salary=user.salary - history.money
        update_user_salary ( id=user.id, salary=updated_salary, db=db )
        db.query ( Kpi_History ).filter ( Kpi_History.id == history.id ).update ( {
            Kpi_History.status: False, } )
        db.commit ( )
        data=NotificationBase (
            money=history.money,
            worker_id=user.id,
            order_id=order.id,
            savdo_id=order.savdo_id,
            user_id=user.id,
            name=user.name,
            type="return_products"
        )
        await manager.send_user ( message=data, user_id=user.id, db=db )
    db.query ( Orders ).filter ( Orders.id == id ).update ( {
        Orders.status: False,
        Orders.order_status: 'return_products',
        Orders.user_id: user.id
    } )
    db.commit ( )
    alls = db.query(Incomes).filter(Incomes.source_id==id).all()
    for i in alls:
        db.query(Incomes).filter(Incomes.id==i.id).delete()
        db.commit ( )
    return {"date": "Mahsulot o'chirildi !"}
