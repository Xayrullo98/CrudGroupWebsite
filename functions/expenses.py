from fastapi import HTTPException
import datetime

from sqlalchemy.orm import joinedload

from functions.trades import one_trade
from functions.users import one_user, update_user_salary, update_user_company_balanse
from models.expenses import Expenses
from models.users import Users
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_expenses(search, status,source_id,start_date,end_date, page, limit, db):
	if search:
		search_formatted = "%{}%".format(search)
		search_filter = Expenses.money.like(search_formatted)
	else:
		search_filter = Expenses.id > 0
	if status in [True, False]:
		status_filter = Expenses.status == status
	else:
		status_filter = Expenses.status.in_([True, False])
	
	if source_id:
		source_id_filter = Expenses.source_id == source_id
	else:
		source_id_filter = Expenses.id > 0
	
	try:
		if not start_date:
			start_date=datetime.date.min
		if not end_date:
			end_date=datetime.date.today()
		end_date=datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
	except Exception as error:
		raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
	
	expenses = db.query(Expenses).options(
		joinedload(Expenses.user_for_expenses).load_only(Users.name,Users.roll,Users.username,Users.number,)).filter(Expenses.date_time > start_date).filter(
		Expenses.date_time <= end_date).filter(search_filter, status_filter,source_id_filter).order_by(Expenses.id.desc())
	if page and limit:
		return pagination(expenses, page, limit)
	else:
		return expenses.all()


def one_expense(id, db):
	return db.query(Expenses).filter(Expenses.id == id).first()


async def create_expense(form,cur_user, db):
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	
	if one_user(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	user=one_user(id=form.source_id, db=db)
	if form.source=="company_balance":
		updated_company_balance = user.company_balance + form.money
		update_user_company_balanse(id=form.source_id, company_balance=updated_company_balance, db=db)
	else:
		updated_salary=user.salary - form.money
		update_user_salary(id=form.source_id, salary=updated_salary, db=db)
	data = NotificationBase(
		money=form.money,
		worker_id=form.source_id,
		user_id=cur_user.id,
		type=form.source)
	await manager.send_user(message=data, user_id=form.source_id, db=db)
	new_expense_db = Expenses(
		money=form.money,
		type=form.type,
		source_id=form.source_id,
		source=form.source,
		user_id=cur_user.id,
	)
	db.add(new_expense_db)
	db.commit()
	 
	return new_expense_db


def update_expense(form,cur_user, db):
	if one_expense(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")
	
	if one_user(cur_user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	if one_trade(form.source_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli savdo mavjud emas")
	
	db.query(Expenses).filter(Expenses.id == form.id).update({
		Expenses.money: form.money,
		Expenses.type: form.type,
		Expenses.source_id: form.source_id,
		Expenses.source: form.source,
		Expenses.user_id: cur_user.id,
		Expenses.status: form.status
	})
	db.commit()
	return one_expense(form.id, db)


def expense_delete(id, db):
	if one_expense(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli expense mavjud emas")
	db.query(Expenses).filter(Expenses.id == id).update({
		Expenses.status: False,
		})
	db.commit()
	return {"date":"Ma'lumot o'chirildi !"}