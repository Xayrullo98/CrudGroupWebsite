from pydantic import BaseModel


class TodoBase(BaseModel):
	work: str
	jarima:float
	worker_id:int


class TodoCreate(TodoBase):
	pass


class TodoUpdate(TodoBase):
	id: int
	status: bool
