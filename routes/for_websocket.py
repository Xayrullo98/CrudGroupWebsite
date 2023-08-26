from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, Depends
from db import SessionLocal, get_db

from jose import jwt
from models.notification import Notification
from models.users import *
from routes.notification import manager
from schemas.users import UserBase, UserCreate
from schemas.notification import NotificationBase, NotificationCreate
from routes.auth import SECRET_KEY, ALGORITHM
from sqlalchemy.orm import Session

notification_router = APIRouter()


# @notification_router.get("/send_to_public")
# async def send_to_public(title: str, description: str, db: Session = Depends(get_db)):
#
#     message = NotificationCreate(
#         title=title,
#         body=description,
#         imgurl="https://api2.f9.crud.uz/images/galery/niso-logo.png"
#     )
#
#     from routes.notification import manager
#     return await manager.send_user(message, 'plant_admin', db)


@notification_router.websocket("/ws/connection")
async def websocket_endpoint(
        token: str,
        websocket: WebSocket,
        db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    user: Users = db.query(Users).filter_by(
        username=username, status=True).first()

    await manager.connect(websocket, user)

    if user:

        for ntf in user.notifications:
            message = NotificationCreate(
                money=ntf.money,
                worker_id=ntf.worker_id,
                order_id=ntf.order_id,
                savdo_id=ntf.savdo_id,
                name=ntf.name,
                type=ntf.type,
                work=ntf.work,
	            deadline=ntf.deadline,
                user_id=ntf.user_id,

            )
            await manager.send_personal_json(message, (websocket, user))
        db.query(Notification).filter_by(worker_id=user.id).delete()
        db.commit()

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
