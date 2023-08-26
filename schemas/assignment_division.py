from pydantic import BaseModel
from pydantic.datetime_parse import date


class AssignmentBase(BaseModel):
    order_id: int
    programmer_type: str
    programmer_title: str
    worker_id: int
    work_price: float
    currency: str
    deadline: date


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(AssignmentBase):
    id: int
    deadline_status: bool
    status: bool
