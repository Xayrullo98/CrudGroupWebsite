from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
import datetime
from functions import orders

from functions.users import one_user
from models.incomes import Incomes
from models.orders import Orders

from models.trades import Trades

from utils.pagination import pagination


def all_trades(search, status, order_id, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Trades.price.like(search_formatted) | Trades.quantity.like(search_formatted)
	else:
		search_filter=Trades.id > 0
	if status in [True, False]:
		status_filter=Trades.status == status
	else:
		status_filter=Trades.status.in_([True, False])

	if order_id:
		order_filter=Trades.order_id == order_id
	else:
		order_filter=Trades.order_id > 0

	trades=db.query(Trades).filter(search_filter, status_filter, order_filter).order_by(
		Trades.id.desc())

	if page and limit:
		return pagination(trades, page, limit)
	else:
		return trades.all()


def one_trade(id, db):
	return db.query(Trades).options(
		joinedload(Trades.products)).filter(
		Trades.id == id).first()
def one_trade_via_order_id(order_id, db):
	return db.query(Trades).filter(
		Trades.order_id == order_id).first()

def create_trade(form, user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")



	if orders.one_order(form.order_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")

	new_trade_db=Trades(
		quantity=form.quantity,
		project_name=form.project_name,
		user_id=user.id,
		order_id=form.order_id,

	)

	db.add(new_trade_db)
	db.commit()
	db.refresh(new_trade_db)
	return new_trade_db


def update_trade(form, user, db):
	if one_trade(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")

	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")



	if orders.one_order(form.order_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli order mavjud emas")

	db.query(Trades).filter(Trades.id == form.id).update({
		Trades.id: form.id,
		Trades.project_name: form.project_name,
		Trades.status: form.status,
		Trades.quantity: form.quantity,
		Trades.user_id: user.id})
	db.commit()
	trades_income = db.query(Incomes).filter(Incomes.source_id==form.id).all()
	money = 0
	for i in trades_income:
		money=money+i.money


	real_money=get_order_id_from_trades ( id=form.order_id, user=user.id, db=db ).get ( 'money' )
	money_real=get_order_id_from_trades ( id=form.order_id, user=user.id, db=db ).get ( 'real_money' )
	rest_summ=real_money - money
	if real_money < money:
		raise HTTPException ( status_code=400,
							  detail=f"Ortiqcha  {-1 * rest_summ} ming so'm to'lov qilinmoqda qayta kiriting" )
	if int ( real_money ) == int ( money ):

		db.query ( Orders ).filter ( Orders.id == form.order_id ).update ( {
			Orders.id: form.order_id,
			Orders.user_id: user.id,
			Orders.order_status: 'design',
			Orders.design_date: datetime.datetime.now ( ).date ( )

		} )
		db.commit ( )


	else:
		db.query ( Orders ).filter ( Orders.id == form.order_id ).update ( {
			Orders.id: form.order_id,
			Orders.user_id: user.id,
			Orders.order_status: 'payment',

		} )
		db.commit ( )

	orders.update_summ ( id=form.order_id, summ=real_money, rest_summ=rest_summ, db=db )
	orders.update_real_summ ( id=form.order_id, summ=money_real, db=db )
	orders.update_payment ( id=form.order_id, money=money, db=db )
	return one_trade(form.id, db)


def filter_trades(order_id, db, status=True):
	if status in [True, False]:
		status_filter=Trades.status == status
	else:
		status_filter=Trades.id > 0

	if order_id:
		order_filter=Trades.order_id == order_id
	else:
		order_filter=Trades.id > 0

	users=db.query(Trades).filter(status_filter, order_filter).order_by(Trades.id.desc())

	return users.all()


def get_order_id_from_trades(id, user, db):
		if orders.one_order(id, db) is None:
			raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli order mavjud emas")

		trades=filter_trades(order_id=id, db=db)

		order=orders.one_order(id=id, db=db)

		summa=0
		for trade in trades:

			summa+=order.real_summ * trade.quantity

		discount = 100 - order.discount
		return {"money": summa * discount / 100,"real_money":summa}


def get_deadline_from_trades(order_id, user_id, db):
	if orders.one_order(order_id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {order_id} raqamli order mavjud emas")
