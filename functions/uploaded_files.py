from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from functions.users import one_user
from models.done import Done
from models.uploaded_files import Uploaded_files
from models.users import Users
import datetime
from utils.pagination import pagination


def all_uploaded_filess(search, status, order_id,source_id, start_date, end_date,source, page, limit, db):
	if search:
		search_formatted="%{}%".format(search)
		search_filter=Uploaded_files.work.like(search_formatted) | \
		              Uploaded_files.jarima.like(search_formatted)
	else:
		search_filter=Uploaded_files.id > 0
	if status in [True, False]:
		status_filter=Uploaded_files.status == status
	else:
		status_filter=Uploaded_files.status.in_([True, False])
	if order_id:
		user_filter=Uploaded_files.source_id == order_id
	else:
		user_filter=Uploaded_files.user_id > 0
	if source_id:
		source_id_filter=Uploaded_files.source_id == source_id
	else:
		source_id_filter=Uploaded_files.user_id > 0
	if source:
		source_filter = Uploaded_files.source==source
	else:
		source_filter = Uploaded_files.id>0
	try:
		if not start_date:
			start_date=datetime.date.min
		
		if not end_date:
			end_date=datetime.date.today()
		end_date=datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
	except Exception as error:
		raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
	uploaded_filess=db.query(Uploaded_files).filter(Uploaded_files.created_on > start_date).filter(
		Uploaded_files.created_on <= end_date).filter(search_filter, status_filter, user_filter,source_filter,source_id_filter).order_by(
		Uploaded_files.id.desc())
	
	if page and limit:
		return pagination(uploaded_filess, page, limit)
	else:
		return uploaded_filess.all()



def one_uploaded_files(id, db):
	return db.query(Uploaded_files).filter(Uploaded_files.id == id).first()

def one_uploaded_file_via_source(source_id,source, db):
	return db.query(Uploaded_files).filter(Uploaded_files.source_id == source_id,Uploaded_files.source==source).first()
def create_uploaded_file(source_id,source, file_url,comment, user, db):
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli foydalanuvchi mavjud emas")

	new_uploaded_files_db=Uploaded_files(
		file=file_url,
		source_id=source_id,
		source=source,
		user_id=user.id,
		comment=comment
	
	)
	db.add(new_uploaded_files_db)
	db.commit()
	db.refresh(new_uploaded_files_db)
	return {"data": "Added"}


def update_uploaded_files(form, user, db):
	if one_uploaded_files(form.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli uploaded_files mavjud emas")
	
	if one_user(user.id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli user mavjud emas")
	
	db.query(Uploaded_files).filter(Uploaded_files.id == form.id).update({
		Uploaded_files.id: form.id,
		Uploaded_files.status: form.status,
		Uploaded_files.work: form.work,
		Uploaded_files.worker_id: form.worker_id,
		Uploaded_files.jarima: form.jarima,
		Uploaded_files.user_id: user.id
	})
	db.commit()
	return one_uploaded_files(form.id, db)


def uploaded_files_delete(id, cur_user, db):
	if one_uploaded_files(id, db) is None:
		raise HTTPException(status_code=400, detail="Bunday id raqamli ma'lumot mavjud emas")
	db.query(Uploaded_files).filter(Uploaded_files.id == id).update({
		Uploaded_files.status: False,
	})
	db.commit()
	return {"date": "Ma'lumot o'chirildi !"}
