from pydantic import BaseModel
from typing import Optional


from pydantic.datetime_parse import date


class Kpi_HistoryBase(BaseModel):
    money: float
    type: str
    order_id: int
    comment: Optional[str]=None



class Kpi_HistoryCreate(Kpi_HistoryBase):
      discount:float=0
      



class Kpi_HistoryUpdate(Kpi_HistoryBase):
    id: int
    status: bool