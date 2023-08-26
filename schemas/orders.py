from pydantic import BaseModel
from typing import Optional
from pydantic.datetime_parse import date


class OrderBase(BaseModel):
	customer_id: int
	comment: Optional[str]



class OrderCreate(OrderBase):
	deadline: date


class OrderUpdate(OrderBase):
	id: int
	status: bool
	deadline:date


class OrderStatusUpdate(BaseModel):
	id:int
	
	
	
