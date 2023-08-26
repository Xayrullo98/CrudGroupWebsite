
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload

from models.kpi import Kpi
from models.orders import Orders

pwd_context=CryptContext(schemes=['bcrypt'])

from fastapi import HTTPException
from models.users import Users

from routes.auth import get_password_hash
from utils.pagination import pagination


def all_users(search, status, roll, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Users.name.like(search_formatted) | Users.number.like(search_formatted) | Users.username.like(
			search_formatted) | Users.roll.like(search_formatted)
	else:
		search_filter=Users.id > 0
	if status in [True, False]:
		status_filter=Users.status == status
	else:
		status_filter=Users.id > 0
	
	if roll:
		roll_filter=Users.roll == roll
	else:
		roll_filter=Users.id > 0
	
	users=db.query(Users).options(joinedload(Users.kpi), joinedload(Users.order.and_(Orders.status==True))).filter(search_filter, status_filter, roll_filter).order_by(Users.name.asc())
	if page and limit:
		return pagination(users, page, limit)
	else:
		return users.all()


def one_user(id, db):
	return db.query(Users).options(joinedload(Users.kpi), joinedload(Users.order.and_(Orders.status==True))).filter(Users.id == id).first()

def one_user_check(id, db):
	return db.query(Users).filter(Users.id == id).first()
def user_current(user, db):
	return db.query(Users).options(joinedload(Users.kpi), joinedload(Users.order.and_(Orders.status==True))).filter(Users.id == user.id).first()

def create_user(form,  db):
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")
	number_verification=db.query(Users).filter(Users.number == form.number).first()
	if number_verification:
		raise HTTPException(status_code=400, detail="Bunday telefon raqami  mavjud")

	new_user_db=Users(
		name=form.name,
		username=form.username,
		number=form.number,
		password=get_password_hash(form.password),
		roll=form.roll,
		status=form.status,
	
	)
	db.add(new_user_db)
	db.commit()
	db.refresh(new_user_db)
	# for kpi in form.kpi:
	# 	new_phone_db = Kpi(
	# 		percentage=kpi.percentage,
	# 		source_id=new_user_db.id,
	# 		user_id=user.id,
	# 	)
	# 	db.add(new_phone_db)
	# 	db.commit()
	return new_user_db


def update_user(form, user, db):
	if one_user(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	user_verification=db.query(Users).filter(Users.username == form.username).first()
	if user_verification and user_verification.id != form.id:
		raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud")

	db.query(Users).filter(Users.id == form.id).update({
		Users.name: form.name,
		Users.username: form.username,
		Users.password: get_password_hash(form.password),
		Users.roll: form.roll,
		Users.status: form.status,
		Users.number: form.number,
		
	})
	db.commit()

	db.query(Kpi).filter(Kpi.source_id == form.id).delete()
	for kpi in form.kpi:
		new_phone_db = Kpi(
			percentage=kpi.percentage,
			source_id=form.id,
			user_id=user.id,
		)
		db.add(new_phone_db)
		db.commit()
	return one_user(form.id, db)


def update_user_salary(id, salary,db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	
	db.query(Users).filter(Users.id == id).update({
		Users.salary: salary,
		
	})
	db.commit()
	return one_user(id, db)


def update_user_company_balanse(id, company_balance, db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")

	db.query(Users).filter(Users.id == id).update({
		Users.company_balance: company_balance,

	})
	db.commit()
	return one_user(id, db)

def update_user_balance(id, balance,db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail=f"Bunday {id} raqamli hodim mavjud emas")
	
	
	db.query(Users).filter(Users.id == id).update({
		Users.balance: balance,
		
	})
	db.commit()
	return one_user(id, db)


def filter_users(roll, db,status=True):
	if status in [True, False]:
		status_filter=Users.status == status
	else:
		status_filter=Users.id > 0
	
	if roll:
		roll_filter=Users.roll == roll
	else:
		roll_filter=Users.id > 0
	
	users=db.query(Users).filter(status_filter, roll_filter).order_by(Users.name.asc())
	
	return users.all()


def user_delete(id, db):
	if one_user(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Users).filter(Users.id == id).update({
		Users.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
