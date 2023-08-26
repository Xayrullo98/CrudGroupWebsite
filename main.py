from db import SessionLocal
from fastapi import FastAPI, Request, Response
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
import traceback

from functions.done import check_todo_workr_result

from functions.other_works import select_other_works_deadline

from routes import auth, users, phones, customers,  orders, trades, kpi, kpi_history, \
    incomes, expenses,  for_websocket, todo, done, extraworks, end_time, other_works, \
     uploaded_files, worker_expenses, attandance, social_media,assignment_division,comment,customer_monitoring,project_division
from db import Base, engine

from fastapi.middleware.cors import CORSMiddleware





Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crud group",
	responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
	           401: {'desription': 'Unauthorized'}}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],

)

app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],

)

app.include_router(
    phones.router_phone,
    prefix='/phone',
    tags=['Phone section'],

)

app.include_router(
    customers.router_customer,
    prefix='/customer',
    tags=['Customer section'],

)


app.include_router(
    orders.router_order,
    prefix='/order',
    tags=['Order section'],

)

app.include_router(
    trades.router_trade,
    prefix='/trade',
    tags=['Trade section'],

)

app.include_router(
    kpi.router_kpi,
    prefix='/kpi',
    tags=['Kpi section'],

)

app.include_router(
    kpi_history.router_kpi_history,
    prefix='/kpi_history',
    tags=['Kpi history section'],

)

app.include_router(
    incomes.router_income,
    prefix='/income',
    tags=['Income section'],

)

app.include_router(
    expenses.router_expense,
    prefix='/expense',
    tags=['Expense section'],

)





app.include_router(
    for_websocket.notification_router,
    prefix='',
    tags=['websocket  section'],

)

app.include_router(
    todo.router_todo,
    prefix='/todo',
    tags=['Todo  section'],

)

app.include_router(
    done.router_done,
    prefix='/done',
    tags=['Done  section'],

)

app.include_router(
    extraworks.router_extrawork,
    prefix='/extraworks',
    tags=['Extraworks  section'],

)

app.include_router(
    end_time.router_end_time,
    prefix='/time',
    tags=['Time  section'],

)

app.include_router(
    other_works.router_other_work,
    prefix='/otherworks',
    tags=['Other works  section'],

)


app.include_router(
    uploaded_files.router_file,
    prefix='/file',
    tags=['File  section'],

)


app.include_router(
    worker_expenses.router_expense,
    prefix='/Worker expenses',
    tags=['Worker expenses  section'],

)

app.include_router(
    attandance.attandance_router,
    prefix='/Attandance',
    tags=['Attandance section'],

)

app.include_router(
    social_media.router_social_media,
    prefix='/social_media',
    tags=['Social media section'],

)

app.include_router(
    assignment_division.router_assignment_division,
    prefix='/assignment_division',
    tags=['Assignment division section'],

)

app.include_router(
    customer_monitoring.router_customer_monitoring,
    prefix='/customer_monitoring',
    tags=['Customer monitoring section'],

)

app.include_router(
    comment.router_comment,
    prefix='/comment',
    tags=['Comment section'],

)
app.include_router(
    project_division.router_project_division,
    prefix='/project_division',
    tags=['Project division section'],

)


# @app.on_event("startup")
# @repeat_every(seconds=3600, wait_first=True)
# async def check():
#     timee = datetime.datetime.now().strftime("%H") == "00"
#
#     if timee:
#         await select_other_works_deadline()
#
#
# @app.on_event("startup")
# @repeat_every(seconds=5, wait_first=True)
# async def check_todo():
#     timee = datetime.datetime.now().strftime("%H") == "12"
#
#     if timee:
#         await check_todo_workr_result()


# @app.on_event("startup")
# @repeat_every(seconds=86400, wait_first=True)
# async def check_planting():
#     if check_orders():
#         await check_orders()
#
#
# @app.on_event("startup")
# @repeat_every(seconds=86400, wait_first=True)
# async def check_planting():
#     if check_controls():
#         await check_controls()
