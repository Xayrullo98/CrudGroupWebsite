from pydantic import BaseModel


class WorkerBase(BaseModel):
    money: float
    type: str
    comment: str=None


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(WorkerBase):
    id: int
    status: bool
