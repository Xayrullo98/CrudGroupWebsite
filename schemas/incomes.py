from pydantic import BaseModel


class IncomeBase(BaseModel):
    money: float
    type: str



class IncomeCreate(IncomeBase):
      source_id: int


class IncomeUpdate(IncomeBase):
    id: int
    source_id: int
    status:bool
