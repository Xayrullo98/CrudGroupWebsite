from pydantic import BaseModel


class DoneBase(BaseModel):
	todo_id:int

class DoneCreate(DoneBase):
	result:bool=None


class DoneUpdate(DoneBase):
	id: int
	status: bool = True

