from pydantic import BaseModel
from pydantic.datetime_parse import date,datetime


class NotificationBase(BaseModel):
    money: float=None
    worker_id: int
    order_id: int=None
    savdo_id: int=None
    user_id: int
    name: str = None
    type: str = None
    work:str = None
    deadline:datetime=None


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(NotificationBase):
    id: int
    status: bool
