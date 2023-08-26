import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions import orders

from models.expenses import Expenses
from models.kpi_history import Kpi_History
from functions.kpi import one_kpi, filter_kpi

from functions.trades import one_trade, one_trade_via_order_id
from functions.orders import one_order, update_summ
from functions.users import one_user, update_user_salary, filter_users, update_user_balance
from models.incomes import Incomes
from models.orders import Orders

from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_incomes(search, status, order_id, customer_id, start_date, end_date, page, limit, db):
    if search:
        search_formatted="%{}%".format ( search )
        search_filter=Incomes.money.like ( search_formatted )
    else:
        search_filter=Incomes.id > 0
    if status in [True, False]:
        status_filter=Incomes.status == status
    else:
        status_filter=Incomes.status.in_ ( [True, False] )

    if order_id:
        order_filter=Incomes.source_id == order_id
    else:
        order_filter=Incomes.source_id > 0

    if customer_id:
        customer_filter=Incomes.user_id == customer_id
    else:
        customer_filter=Incomes.user_id > 0

    try:
        if not start_date:
            start_date=datetime.date.min
        if not end_date:
            end_date=datetime.date.today ( )
        end_date=datetime.datetime.strptime ( str ( end_date ), '%Y-%m-%d' ).date ( ) + datetime.timedelta ( days=1 )
    except Exception as error:
        raise HTTPException ( status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  " )

    incomes=db.query ( Incomes ).options (
        joinedload ( Incomes.order ) ).filter ( Incomes.date_time > start_date ).filter (
        Incomes.date_time <= end_date ).filter ( search_filter, status_filter, order_filter,
                                                 customer_filter ).order_by (
        Incomes.id.desc ( ) )
    if page and limit:
        return pagination ( incomes, page, limit )

    else:
        return incomes.all ( )


def one_income(id, db):
    return db.query ( Incomes ).options (
        joinedload ( Incomes.order ).load_only ( Orders.savdo_id, ) ).filter ( Incomes.id == id ).first ( )


async def create_income(form, cur_user, db):
    if one_user ( cur_user.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas" )
    user = one_user ( cur_user.id, db )
    if not user.kpi:
        raise HTTPException(status_code=400, detail="Bu userga kpi yaratilmagan kpi yarating")

    if one_order ( form.source_id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli savdo mavjud emas" )

    order=one_order ( id=form.source_id, db=db )
    rest_summ=order.rest_summ - form.money
    if rest_summ < 0:
        raise HTTPException ( status_code=400,
                              detail=f"Ortiqcha  {-1 * rest_summ} ming so'm to'lov qilinmoqda qayta kiriting" )
    payment_money=form.money + order.payment_summ
    orders.update_payment ( id=form.source_id, money=payment_money, db=db )
    summ=order.summ
    if rest_summ == 0:
        db.query ( Orders ).filter ( Orders.id == form.source_id ).update ( {
            Orders.id: form.source_id,
            Orders.user_id: cur_user.id,
            Orders.order_status: 'design',
            Orders.design_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        update_summ ( id=form.source_id, summ=summ, rest_summ=0, db=db )
        trade=one_trade_via_order_id ( order_id=form.source_id, db=db )

    else:
        update_summ ( id=form.source_id, summ=summ, rest_summ=rest_summ, db=db )

    new_income_db=Incomes (
        money=form.money,
        type=form.type,
        source_id=form.source_id,
        user_id=cur_user.id,

    )
    db.add ( new_income_db )
    db.commit ( )
    db.refresh ( new_income_db )
    # user salary section
    get_order=one_order ( id=form.source_id, db=db )
    user_kpi=filter_kpi ( source_id=cur_user.id, db=db )
    user_money=user_kpi.percentage * form.money / 100
    user=one_user ( id=cur_user.id, db=db )
    updated_salary=user.salary + user_money
    update_user_salary ( id=cur_user.id, salary=updated_salary, db=db )
    updated_balance=user.balance - user_money
    update_user_balance ( id=cur_user.id, balance=updated_balance, db=db )
    new_history_db=Kpi_History (
        money=user_money,
        type=form.type,
        order_id=form.source_id,
        comment='',
        user_id=cur_user.id,
        return_date=datetime.datetime.now ( ), )
    db.add ( new_history_db )
    db.commit ( )
    db.refresh ( new_history_db )
    data=NotificationBase (
        money=user_money,
        worker_id=user.id,
        order_id=form.source_id,
        savdo_id=get_order.savdo_id,
        user_id=cur_user.id,
        name=user.name,
        type="trade"
    )
    await manager.send_user ( message=data, user_id=user.id, db=db )

    users=filter_users ( roll='worker', db=db )
    warehouseman=filter_users ( roll='warehouseman', db=db )
    technologist=filter_users ( roll='technologist', db=db )
    seller_admin=filter_users ( roll='seller_admin', db=db )
    users=users + warehouseman + technologist + seller_admin

    for worker in users:
        worker_kpi=filter_kpi ( source_id=worker.id, db=db )
        worker_money=worker_kpi.percentage * form.money / 100
        user=one_user ( id=worker.id, db=db )
        updated_salary=user.salary + worker_money
        update_user_salary ( id=worker.id, salary=updated_salary, db=db )
        updated_balance=user.balance - worker_money
        update_user_balance ( id=worker.id, balance=updated_balance, db=db )
        new_history_db=Kpi_History (
            money=worker_money,
            type=form.type,
            order_id=form.source_id,
            comment='',
            user_id=worker.id,
            return_date=datetime.datetime.now ( ) )
        db.add ( new_history_db )
        db.commit ( )
        data=NotificationBase (
            money=worker_money,
            worker_id=worker.id,
            order_id=form.source_id,
            savdo_id=get_order.savdo_id,
            user_id=cur_user.id,
            name=user.name,
            type="trade"
        )
        await manager.send_user ( message=data, user_id=worker.id, db=db )

    return new_income_db


def update_income(form, cur_user, db):
    if one_income ( form.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli income mavjud emas" )

    if one_user ( cur_user.id, db ) is None:
        raise HTTPException ( status_code=400, detail="Bunday id raqamli user mavjud emas" )

    db.query ( Incomes ).filter ( Incomes.id == form.id ).update ( {
        Incomes.money: form.money,
        Incomes.type: form.type,
        Incomes.source_id: form.source_id,
        Incomes.user_id: cur_user.id,
        Incomes.status: form.status
    } )
    db.commit ( )
    return one_income ( form.id, db )


def result_of_incomes_and_expenses(start_date, end_date, today, db):
    if not today:
        try:
            if not start_date:
                start_date=datetime.date.min
            if not end_date:
                end_date=datetime.date.today ( )
            end_date=datetime.datetime.strptime ( str ( end_date ), '%Y-%m-%d' ).date ( ) + datetime.timedelta (
                days=1 )
        except Exception as error:
            raise HTTPException ( status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  " )
        # incomes
        profits=db.query ( Incomes ).filter ( Incomes.date_time > start_date ).filter (
            Incomes.date_time < end_date ).all ( )
        profit_money=sum ( [profit.money for profit in profits] )
        # expenses
        salary_expenses=Expenses.source == 'salary'

        expenses_for_salary=db.query ( Expenses ).filter ( Expenses.date_time > start_date ).filter (
            Expenses.date_time < end_date ).filter ( salary_expenses ).all ( )
        expences_money_for_salary=sum ( [expense.money for expense in expenses_for_salary] )

        company_expenses=Expenses.source == 'company_balance'
        expenses_for_company_balance=db.query ( Expenses ).filter ( Expenses.date_time > start_date ).filter (
            Expenses.date_time < end_date ).filter ( company_expenses ).all ( )
        expences_money_for_company_balance=sum ( [expense.money for expense in expenses_for_company_balance] )
        real_profit=profit_money - expences_money_for_company_balance - expences_money_for_salary
        return dict ( profit=real_profit, salary_expenses=expences_money_for_salary, income=profit_money,
                      company_balance_expenses=expences_money_for_company_balance )
    else:
        try:

            start_date=datetime.datetime.strptime ( str ( today ), '%Y-%m-%d' ).date()
            end_date=datetime.datetime.strptime ( str ( start_date ), '%Y-%m-%d' ).date ( ) + datetime.timedelta (
                days=1 )
        except Exception as error:
            raise HTTPException ( status_code=400, detail=f"Faqat yyyy-mmm-dd formatida yozing  {error} " )
        profits=db.query ( Incomes ).filter ( Incomes.date_time >= start_date ).filter (
            Incomes.date_time < end_date ).all ( )
        profit_money=sum ( [profit.money for profit in profits] )
        # expenses
        salary_expenses=Expenses.source == 'salary'

        expenses_for_salary=db.query ( Expenses ).filter ( Expenses.date_time >= start_date ).filter (
            Expenses.date_time < end_date ).filter ( salary_expenses ).all ( )
        expences_money_for_salary=sum ( [expense.money for expense in expenses_for_salary] )

        company_expenses=Expenses.source == 'company_balance'
        expenses_for_company_balance=db.query ( Expenses ).filter ( Expenses.date_time >= start_date ).filter (
            Expenses.date_time < end_date ).filter (
            company_expenses ).all ( )

        expences_money_for_company_balance=sum ( [expense.money for expense in expenses_for_company_balance] )
        real_profit=profit_money - expences_money_for_company_balance - expences_money_for_salary
        return dict ( profit=real_profit, salary_expenses=expences_money_for_salary, income=profit_money,
                      company_balance_expenses=expences_money_for_company_balance )
