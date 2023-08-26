# import math
#
# from sqlalchemy import or_, and_
# from sqlalchemy.orm import joinedload, Session, Load
# from fastapi import HTTPException
# from models.attandance import *
# from models.users import *
# import datetime
# from schemas.attandance import *
# import uuid
# import datetime
#
# from utils.pagination import pagination
#
#
# async def makeDavomat(user_id, type, dateTime, authorizator_name, db: Session):
#     # with open ( f"./hik_logs/{uuid.uuid4 ( )}.txt", "w" ) as f:
#     #     f.write ( f"UserNAME:Yusufjon DATE:2023-203" )
#
#     user = db.query(Users).filter_by(id=user_id).first()
#     if not user:
#         raise HTTPException(status_code=400, detail="Hodim topilmadi!")
#
#     if type == 'entry':
#         new_dav = Attandance(
#             type='entry',
#             user_id=user_id,
#             authorizator=authorizator_name,
#             datetime=dateTime,
#         )
#         db.add(new_dav)
#         db.commit()
#         db.refresh(new_dav)
#     elif type == 'exit':
#
#         last_entry = db.query(Attandance).filter(Attandance.type == 'entry',
#                                                      Attandance.user_id == user_id).order_by(
#                 Attandance.id.desc()).first()
#         day = str(last_entry.datetime)
#         date_object = datetime.datetime.strptime(str(day), '%Y-%m-%d %H:%M:%S')
#
#         today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#         date_format_str = '%Y-%m-%d %H:%M:%S'
#
#         date_1 = str(date_object)
#         date_2 = str(today)
#
#         start = datetime.datetime.strptime(date_1, date_format_str)
#         end = datetime.datetime.strptime(date_2, date_format_str)
#
#         diff = end - start
#
#         # Get interval between two timstamps as timedelta object
#         diff_in_hours = diff.total_seconds() // 3600
#
#         diff_in_minut = diff.total_seconds() % 3600 // 60 // 1
#
#         diff_in_secund = diff.total_seconds() % 60 // 1
#
#         def check_format(value):
#             return (f"0{int(value)}" if 0 <= value <= 9 else str(int(value)))
#
#         d = f"{check_format(diff_in_hours)}:{check_format(diff_in_minut)}:{check_format(diff_in_secund)}"
#         new_dav = Attandance(
#             type='exit',
#             user_id=user_id,
#             working_period=d,
#             authorizator=authorizator_name,
#             datetime=dateTime,
#         )
#         db.add(new_dav)
#         db.commit()
#         db.refresh(new_dav)
#
#         raise HTTPException(status_code=400, detail="Bunday type mavjud emas ")
#
#
#
#
#
# def get_all_attandances(search, user_id, start_date, end_date, date, page, limit, usr, db: Session):
#     if search:
#         search_formatted = "%{}%".format(search)
#         search_filter = Attandance.authorizator.like(search_formatted)
#     else:
#         search_filter = Attandance.id > 0
#
#     if user_id:
#         user_filter = Attandance.user_id == user_id
#     else:
#         user_filter = Attandance.user_id > 0
#     try:
#
#         end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
#     except Exception as error:
#         raise HTTPException(status_code=400, detail=f"Faqat yyyy-mmm-dd formatida yozing {error} ")
#     other_work = db.query(Attandance).options(
#         joinedload(Attandance.user)).filter(
#         Attandance.datetime > start_date).filter(
#         Attandance.datetime <= end_date).filter(search_filter, user_filter)
#
#     if date:
#         other_work = other_work.filter(func.date(Attandance.datetime) == date)
#
#     other_work = other_work.order_by(Attandance.id.desc())
#
#     if page and limit:
#         return pagination(other_work, page, limit)
#     else:
#         return other_work.all()
#
#
# def get_attandances_via_user_id(user_id, start_date, end_date, db: Session):
#     if user_id:
#         # user_id_status=Attandance.user_id == user_id
#         try:
#             pass
#             end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
#         except Exception as error:
#             raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")
#
#         users = db.query(Users).options(joinedload(
#             Users.attandances.and_(Attandance.datetime > start_date, Attandance.datetime <= end_date,
#                                    Attandance.user_id == user_id))).filter(Users.id == user_id).all()
#
#         return users
#
#
# def update_attandance(id, form_data: UpdateAttandance, usr, db: Session):
#     attandance = db.query(Attandance).filter(Attandance.id == id)
#     this_attandance = attandance.first()
#     if this_attandance:
#         attandance.update({
#             Attandance.type: form_data.type,
#             Attandance.user_id: form_data.user_id,
#             Attandance.working_period: form_data.working_period,
#             Attandance.authorizator: form_data.authorizator,
#             Attandance.datetime: form_data.datetime,
#         })
#         db.commit()
#
#         raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
#     else:
#         raise HTTPException(status_code=400, detail="So`rovda xatolik!")
import math

from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload, Session, Load
from fastapi import HTTPException
from models.attandance import *
from models.users import *
import datetime
from schemas.attandance import *
import uuid
import datetime

from utils.pagination import pagination


async def makeDavomat(user_id, type, dateTime, authorizator_name, db: Session):
    # with open ( f"./hik_logs/{uuid.uuid4 ( )}.txt", "w" ) as f:
    #     f.write ( f"UserNAME:Yusufjon DATE:2023-203" )

    user = db.query(Users).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Hodim topilmadi!")
    if type == 'entry':
        new_dav = Attandance(
            type='entry',
            user_id=user_id,
            authorizator=authorizator_name,
            datetime=dateTime,
        )
        db.add(new_dav)
        db.commit()
        db.refresh(new_dav)
    elif type == 'exit':
        try:
            last_entry = db.query(Attandance).filter(Attandance.type == 'entry',
                                                     Attandance.user_id == user_id).order_by(
                Attandance.id.desc()).first()
            day = str(last_entry.datetime)
            date_object = datetime.datetime.strptime(str(day), '%Y-%m-%d %H:%M:%S')

            today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            date_format_str = '%Y-%m-%d %H:%M:%S'

            date_1 = str(date_object)
            date_2 = str(today)

            start = datetime.datetime.strptime(date_1, date_format_str)
            end = datetime.datetime.strptime(date_2, date_format_str)

            diff = end - start

            # Get interval between two timstamps as timedelta object
            diff_in_hours = diff.total_seconds() // 3600

            diff_in_minut = diff.total_seconds() % 3600 // 60 // 1

            diff_in_secund = diff.total_seconds() % 60 // 1

            def check_format(value):
                return (f"0{int(value)}" if 0 <= value <= 9 else str(int(value)))

            d = f"0000-00-00T{check_format(diff_in_hours)}:{check_format(diff_in_minut)}:{check_format(diff_in_secund)}"
            new_dav = Attandance(
                type='exit',
                user_id=user_id,
                working_period=d,
                authorizator=authorizator_name,
                datetime=dateTime,
            )
            db.add(new_dav)
            db.commit()
            db.refresh(new_dav)
        except Exception as x:
            raise HTTPException(status_code=400, detail=f"{x}")

def get_all_attandances(search, user_id, start_date, end_date, date, page, limit, usr, db: Session):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Attandance.authorizator.like(search_formatted)
    else:
        search_filter = Attandance.id > 0

    if user_id:
        user_filter = Attandance.user_id == user_id
    else:
        user_filter = Attandance.user_id > 0
    try:

        end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Faqat yyyy-mmm-dd formatida yozing {error} ")
    other_work = db.query(Attandance).options(
        joinedload(Attandance.user)).filter(
        Attandance.datetime > start_date).filter(
        Attandance.datetime <= end_date).filter(search_filter, user_filter)

    if date:
        other_work = other_work.filter(func.date(Attandance.datetime) == date)

    other_work = other_work.order_by(Attandance.id.desc())

    if page and limit:
        return pagination(other_work, page, limit)
    else:
        return other_work.all()


def get_attandances_via_user_id(user_id, start_date, end_date, db: Session):
    if user_id:
        # user_id_status=Attandance.user_id == user_id
        try:
            pass
            end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d').date() + datetime.timedelta(days=1)
        except Exception as error:
            raise HTTPException(status_code=400, detail="Faqat yyyy-mmm-dd formatida yozing  ")

        users = db.query(Users).options(joinedload(
            Users.attandances.and_(Attandance.datetime > start_date, Attandance.datetime <= end_date,
                                   Attandance.user_id == user_id))).filter(Users.id == user_id).all()

        return users


def update_attandance(id, form_data: UpdateAttandance, usr, db: Session):
    attandance = db.query(Attandance).filter(Attandance.id == id)
    this_attandance = attandance.first()
    if this_attandance:
        attandance.update({
            Attandance.type: form_data.type,
            Attandance.user_id: form_data.user_id,
            Attandance.working_period: form_data.working_period,
            Attandance.authorizator: form_data.authorizator,
            Attandance.datetime: form_data.datetime,
        })
        db.commit()

        raise HTTPException(status_code=200, detail="O`zgarish saqlandi!")
    else:
        raise HTTPException(status_code=400, detail="So`rovda xatolik!")