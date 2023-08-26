from typing import Optional

from pydantic import BaseModel
from pydantic.datetime_parse import  time



class End_time_Base(BaseModel):
    date : Optional[time]=time.min


class End_time_Create(End_time_Base):
    pass


class End_time_Update(End_time_Base):
    id: int
    status: bool = True
