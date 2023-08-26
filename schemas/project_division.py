from pydantic import BaseModel
from pydantic.datetime_parse import date


class Project_divisionBase(BaseModel):
    order_id: int
    text: str
    deadline: date
    worker_id: int


class Project_divisionCreate(Project_divisionBase):
    pass


class Project_divisionUpdate(Project_divisionBase):
    id: int
    status: bool
