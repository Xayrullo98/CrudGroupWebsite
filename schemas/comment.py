from pydantic import BaseModel


class CommentBase(BaseModel):
	customer_id:int
	customer_monitoring_id:int
	text:str

class CommentCreate(CommentBase):
	pass


class CommentUpdate(CommentBase):
	id: int
	status: bool = True

