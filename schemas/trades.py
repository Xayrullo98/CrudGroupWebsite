
from pydantic import BaseModel



class TradeBase(BaseModel):
    project_name: str
    quantity: float = 1
    


class TradeCreate(TradeBase):
     order_id: int


class TradeUpdate(TradeBase):
    id: int
    order_id: int
    status:bool

