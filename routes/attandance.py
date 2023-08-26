from fastapi import HTTPException, APIRouter, Depends, Request
from typing import Optional, List
from schemas.users import UserCreate, UserCurrent
from routes.auth import get_current_active_user
from db import SessionLocal, get_db
from sqlalchemy.orm import joinedload, Session
from models.attandance import *
from functions.attandance import *
from schemas.attandance import *
from pydantic.datetime_parse import date
import json
import uuid
import datetime
import traceback

attandance_router = APIRouter()


@attandance_router.get("/")
async def get_attandances(
        search: Optional[str] = "",
        user_id: Optional[int] = 0,
        start_date: Optional[date] = datetime.datetime.min.date(),
        end_date: Optional[date] = datetime.datetime.today().date(),
        date: Optional[date] = None,
        page: Optional[int] = 1,
        limit: Optional[int] = 10,
        db: Session = Depends(get_db),
        usr: UserCurrent = Depends(
            get_current_active_user)):
    return get_all_attandances(search=search, user_id=user_id, date=date, page=page, limit=limit, db=db,
                               start_date=start_date, end_date=end_date, usr=usr)


@attandance_router.get("/user_id")
async def get_attandances_user(

        user_id,
        start_date: Optional[date] = datetime.datetime.min.date(),
        end_date: Optional[date] = datetime.datetime.today().date(),

        db: Session = Depends(get_db),
        usr: UserCurrent = Depends(
            get_current_active_user)):
    return get_attandances_via_user_id(user_id=user_id, db=db,
                                       start_date=start_date, end_date=end_date, )


@attandance_router.post("/create")
async def cretae_attandances(
        type: AttType,
        form_datas: List[NewAttandance],
        db: Session = Depends(get_db),
        usr: UserCurrent = Depends(get_current_active_user)):
    for form_data in form_datas:
        await makeDavomat(user_id=usr.id, type=type,
                          dateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          authorizator_name=usr.name, db=db, )
    return HTTPException(status_code=200, detail=f"Ma'lumotlar saqlandi!")


@attandance_router.get("/users")
async def get_attandance_user(
        search: Optional[str] = "",
        db: Session = Depends(get_db),
        usr: UserCurrent = Depends(
            get_current_active_user)):
    if usr.roll in ['admin', 'seller', 'seller_admin']:
        if search:
            search_formatted = "%{}%".format(search)
            search_filter = Users.username.like(search_formatted) | Users.name.like(
                search_formatted)
            users = db.query(Users).options(joinedload(Users.attandances)).filter(search_filter).all()

            return users
    else:
        raise HTTPException(status_code=400, detail="Sizga ruxsat berilmagan!")



@attandance_router.post("/face-id")
async def get_attandance_users_list(
        req: Request,
        db: Session = Depends(get_db),
):
    try:
        data = await req.body()
        data_str = data.decode()
        data_str = data_str.split("\n", 3)[3]
        data_str = data_str[:-20]

        try:
            data_dict = json.loads(data_str)
            AccessControllerEvent = data_dict['AccessControllerEvent']
            user_id = AccessControllerEvent['employeeNoString']
            attendanceStatus = AccessControllerEvent['attendanceStatus']
            deviceName = AccessControllerEvent['deviceName']

            date_str = data_dict['dateTime']
            date_obj = datetime.datetime.fromisoformat(date_str[:-6])  # remove timezone offset
            formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

            if user_id:
                try:
                    user_id = int(user_id)
                    if user_id > 0:

                        with open(f"./hik_logs/{uuid.uuid4()}.json", "w") as f:
                            f.write(data_str)

                        if attendanceStatus == 'checkIn':
                            type = 'entry'
                        else:
                            type = 'exit'

                        if attendanceStatus:
                            await makeDavomat(user_id=user_id, type=type, dateTime=formatted_date,
                                              authorizator_name=deviceName, db=db, )

                except Exception as e:
                    error_details = traceback.format_exc().split("File")[-1]
        except Exception as e:
            error_details = traceback.format_exc().split("File")[-1]
            with open(f"{uuid.uuid4()}.json", "w") as f:
                f.write(error_details)
        return "success"
    except Exception as e:
        print(e)
        error_details = traceback.format_exc().split("File")[-1]
        # with open(f"{uuid.uuid4()}.json", "w") as f:
        #         f.write(error_details)
        return 1
