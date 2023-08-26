from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload


from functions.users import one_user
from models.done import Done
from models.todo import Todo
from models.users import Users
import datetime
from utils.pagination import pagination


def all_todos(search, status,user_id,start_date,end_date, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Todo.work.like(search_formatted) | \
		              Todo.jarima.like(search_formatted)
	else:
		search_filter=Todo.id > 0
	if status in [True, False]:
		status_filter=Todo.status == status
	else:
		status_filter=Todo.status.in_([True, False])
	if user_id:
		user_filter = Todo.worker_id==user_id
	else:
		user_filter = Todo.user_id>0
	try:
		if not start_date:
			start_date=datetime.date.min
		
		if not end_date:
			end_date=datetime.date.today()
		end_date=datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
	except Exception as error:
		raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
	todos=db.query(Todo).options(
		joinedload(Todo.worker).load_only(Users.name)).filter(Todo.date > start_date).filter(
        Todo.date <= end_date).filter(search_filter, status_filter,user_filter).order_by(Todo.id.desc())

	if page and limit:
		return pagination(todos, page, limit)
	else:
		return todos.all()


def one_todo(id, db):
	return db.query(Todo).filter(Todo.id == id).first()


def create_todo(form, user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")
	

	
	new_todo_db=Todo(
		work=form.work,
		worker_id=form.worker_id,
		jarima=form.jarima,
		user_id=user.id,
	
	)
	db.add(new_todo_db)
	db.commit()
	db.refresh(new_todo_db)
	return new_todo_db


def update_todo(form, user, db):
	if one_todo(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli todo mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	
	
	db.query(Todo).filter(Todo.id == form.id).update({
		Todo.id: form.id,
		Todo.status: form.status,
		Todo.work: form.work,
		Todo.worker_id: form.worker_id,
		Todo.jarima: form.jarima,
		Todo.user_id: user.id
	})
	db.commit()
	return one_todo(form.id, db)





def todo_delete(id,cur_user, db):
	if one_todo(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Todo).filter(Todo.id == id).update({
		Todo.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
