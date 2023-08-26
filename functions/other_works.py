import datetime

from sqlalchemy import and_

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from db import SessionLocal
from functions.users import one_user, update_user_salary, one_user_check
from models.extra import Extra
from models.other_works import OtherWorks
from models.todo import Todo
from models.users import Users
from routes.notification import manager
from schemas.notification import NotificationBase

from utils.pagination import pagination


def all_other_works(search, status, user_id, start_date, end_date, result, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=OtherWorks.work.like(search_formatted)
	else:
		search_filter=OtherWorks.id > 0
	if status in [True, False]:
		status_filter=OtherWorks.status == status
	else:
		status_filter=OtherWorks.status.in_([True, False])
	
	if result in [True, False]:
		result_filter=OtherWorks.result == result
	else:
		result_filter=OtherWorks.id > 0
	if user_id:
		user_filter=OtherWorks.worker_id == user_id
	else:
		user_filter=OtherWorks.worker_id > 0
	
	try:
		if not start_date:
			start_date=datetime.date.min
		
		if not end_date:
			end_date=datetime.date.today()
		end_date=datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
	except Exception as error:
		raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
	other_work=db.query(OtherWorks).options(
		joinedload(OtherWorks.user).load_only(Users.name, Users.username)).filter(OtherWorks.date > start_date).filter(
		OtherWorks.date <= end_date).filter(search_filter, status_filter, user_filter, result_filter).order_by(
		OtherWorks.id.desc())
	
	if page and limit:
		return pagination(other_work, page, limit)
	else:
		return other_work.all()


def one_other_work(id, db):
	return db.query(OtherWorks).options(
		joinedload(OtherWorks.user).load_only(Users.name, Users.username)).filter(OtherWorks.id == id).first()


def select_other_work(user, page, limit, db):
	other_work=db.query(OtherWorks).filter(OtherWorks.user_id == user.id)
	if page and limit:
		return pagination(other_work, page, limit)
	else:
		return other_work.all()


async def select_other_works_deadline():
	db: Session=SessionLocal()
	try:
		deadline=datetime.datetime.now().strftime("%Y-%m-%d")
		
		other_work=db.query(OtherWorks).filter((OtherWorks.deadline >= deadline)).filter(OtherWorks.status==True).all()
		
		for worker in other_work:
				one_work = one_other_work(id=worker.id,db=db)
				
				new_extra_db=Extra(
					money=one_work.jarima,
					type="fine",
					source_id=one_work.worker_id,
					source="Maxsus ishdan",
					user_id=1,
					comment=f"{one_work.work}  bajarilmaganligi uchun"
				
				)
				db.add(new_extra_db)
				db.commit()
				db.query(OtherWorks).filter(OtherWorks.id == one_work.id).update({
					OtherWorks.result: False,
					OtherWorks.status: False
				})
				db.commit()
				worker_user=one_user(id=one_work.worker_id, db=db)
				new_salary=worker_user.salary - one_work.jarima
				update_user_salary(id=worker_user.id, salary=new_salary, db=db)
				try:
					data=NotificationBase(
						money=one_work.jarima,
						worker_id=worker_user.id,
						user_id=1,
						type="fine_for_work",
						name=worker_user.name,
						work=one_work.work
					)
					await manager.send_user(message=data, user_id=worker_user.id, db=db, )
				except Exception as s:
					print(s, )
	
	except Exception as x:
		raise HTTPException(status_code=401, detail=f"{x}")
	finally:
		db.close()


async def create_other_work(form, user, db):
	if one_user(form.worker_id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ishchi mavjud emas")

	worker_name=one_user_check(id=form.worker_id, db=db)
	data=NotificationBase(
		worker_id=form.worker_id,
		user_id=user.id,
		name=worker_name.name,
		type="work",
		work=form.work,
		deadline=form.deadline
	)
	await manager.send_user(message=data, user_id=form.worker_id, db=db)
	new_other_work_db=OtherWorks(
		work=form.work,
		jarima=form.jarima,
		worker_id=form.worker_id,
		deadline=form.deadline,
		user_id=user.id,
	
	)
	db.add(new_other_work_db)
	db.commit()
	db.refresh(new_other_work_db)
	return new_other_work_db


def update_other_work(form, user, db):
	if one_other_work(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli other_work mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	db.query(OtherWorks).filter(OtherWorks.id == form.id).update({
		OtherWorks.id: form.id,
		OtherWorks.status: form.status,
		OtherWorks.work: form.work,
		OtherWorks.jarima: form.jarima,
		OtherWorks.user_id: user.id
	})
	db.commit()
	return one_other_work(form.id, db)


def other_work_delete(id, cur_user, db):
	if one_other_work(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(OtherWorks).filter(OtherWorks.id == id).update({
		OtherWorks.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}


async def other_work_result(id, result, cur_user, db):
	if one_other_work(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	if not result:
		work=one_other_work(id=id, db=db)
		new_extra_db=Extra(
			money=work.jarima,
			type="fine",
			source_id=work.worker_id,
			source="Maxsus ishdan",
			user_id=cur_user.id,
			comment=f"{work.work}  bajarilmaganligi uchun"
		
		)
		db.add(new_extra_db)
		db.commit()
		worker=one_user(id=work.worker_id, db=db)
		new_salary=worker.salary - work.jarima
		update_user_salary(id=work.worker_id, salary=new_salary, db=db)
		
		data=NotificationBase(
			money=work.jarima,
			worker_id=work.worker_id,
			user_id=cur_user.id,
			type="fine_for_work",
			name=worker.name,
			work=work.work
		)
		await manager.send_user(message=data, user_id=work.worker_id, db=db, )
	
	db.query(OtherWorks).filter(OtherWorks.id == id).update({
		OtherWorks.result: result,
		OtherWorks.status: False
	})
	db.commit()
	return {"date": "Done !"}
