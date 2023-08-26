from pydantic import BaseModel
from pydantic.datetime_parse import datetime


class OtherWorksBase(BaseModel):
	work: str
	deadline: datetime
	worker_id: int
	jarima: float


class OtherWorksCreate(OtherWorksBase):
	pass


class OtherWorksUpdate(OtherWorksBase):
	id: int
	status: bool=True
