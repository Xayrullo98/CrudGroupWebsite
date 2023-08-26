import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from db import SessionLocal
from functions.todo import one_todo
from functions.users import one_user, update_user, update_user_salary
from models.done import Done
from models.extra import Extra
from models.todo import Todo
from routes.notification import manager
from schemas.notification import NotificationBase
from utils.pagination import pagination


def all_dones(search, status, start_date, end_date, page, worker_id, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Done.todo_id.like(search_formatted)
	else:
		search_filter=Done.id > 0
	if status in [True, False]:
		status_filter=Done.status == status
	else:
		status_filter=Done.status.in_([True, False])
	if worker_id:
		work_filter=Done.user_id == worker_id
	else:
		work_filter=Done.user_id > 0
	try:
		if not start_date:
			start_date=datetime.date.min
		if not end_date:
			end_date=datetime.date.today()
		end_date=datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
	except Exception as error:
		raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
	dones=db.query(Done).options(
		joinedload(Done.todo).load_only(Todo.work)).filter(Done.date > start_date).filter(
		Done.date <= end_date).filter(search_filter, status_filter, work_filter).order_by(Done.id.desc())
	if page and limit:
		return pagination(dones, page, limit)
	else:
		return dones.all()


def one_done(id, db):
	return db.query(Done).options(
		joinedload(Done.todo).load_only(Todo.work)).filter(Done.id == id).first()


async def create_done(form, user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	todo_work=one_todo(id=form.todo_id, db=db)
	new_done_db=Done(
		todo_id=form.todo_id,
		user_id=todo_work.worker_id,
		result=form.result
	
	)
	db.add(new_done_db)
	db.commit()
	db.refresh(new_done_db)
	if not form.result:
		todoo=one_todo(id=form.todo_id, db=db)
		
		new_extra_db=Extra(
			money=todoo.jarima,
			type='fine',
			source_id=todo_work.worker_id,
			source='work',
			user_id=todo_work.worker_id,
			comment=f'{todoo.work} bajarilmaganligi uchun')
		db.add(new_extra_db)
		db.commit()
		worker=one_user(id=todo_work.worker_id, db=db)
		new_salary=worker.salary - todoo.jarima
		update_user_salary(id=todo_work.worker_id, salary=new_salary, db=db)

		data=NotificationBase(
			money=todo_work.jarima,
			worker_id=todo_work.worker_id,
			user_id=user.id,
			type="fine_for_work",
			work=todo_work.work
		)
		await manager.send_user(message=data, user_id=todo_work.worker_id, db=db, )

	return new_done_db


def update_done(form, user, db):
	if one_done(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli done mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	db.query(Done).filter(Done.id == form.id).update({
		Done.id: form.id,
		Done.status: form.status,
		Done.todo_id: form.todo_id,
		Done.user_id: user.id
	})
	db.commit()
	return one_done(form.id, db)


def done_delete(id, cur_user, db):
	if one_done(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Done).filter(Done.id == id).update({
		Done.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}


async def check_todo_workr_result():
	db: Session=SessionLocal()
	try:
		
		todo_works=db.query(Done).filter(Done.result == None).all()
		for worker in todo_works:
			todo=one_todo(id=worker.todo_id, db=db)
			
			new_extra_db=Extra(
				money=todo.jarima,
				type="fine",
				source_id=worker.todo_id,
				source="work",
				user_id=1,
				comment=f"{worker.todo_id} id raqamli ish  bajarilmaganligi uchun"
			
			)
			db.add(new_extra_db)
			db.commit()
			db.query(Done).filter(Done.id == worker.id).update({
				Done.result: False,
				
			})
			db.commit()
			worker_user=one_user(id=worker.user_id, db=db)
			new_salary=worker_user.salary - todo.jarima
			update_user_salary(id=worker_user.id, salary=new_salary, db=db)
			
			data=NotificationBase(
				money=todo.jarima,
				worker_id=worker_user.id,
				user_id=worker.user_id,
				type="fine_for_work",
				name=worker_user.name,
			
			)
			await manager.send_user(message=data, user_id=worker_user.id, db=db, )
	
	
	except Exception as x:
		raise HTTPException(status_code=401, detail=f"{x}")
	finally:
		db.close()
