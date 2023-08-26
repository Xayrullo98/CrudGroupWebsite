from fastapi import Depends, HTTPException
from pydantic import BaseModel,validator
from typing import Optional, List

from sqlalchemy.orm import Session

from db import get_db, SessionLocal
from models.users import Users
from schemas.kpi import KpiBase

db: Session=SessionLocal ( )
class UserBase(BaseModel):
    name: str
    username: str
    roll: str
    status: bool


class UserCreate(UserBase):
    password: str
    number: str
    kpi:List[KpiBase]


    # @validator ( 'number' )
    # def phone_validate(cls, v):
    #     validate_my=db.query ( Users ).filter (
    #         Users.number == v,
    #     ).count ( )
    #
    #     # if validate_my != 0:
    #     #     raise HTTPException ( status_code=400,detail='Bunday telefon raqami avval ro`yxatga olingan.' )
    # #   if len ( v ) != 13:
    # #         raise HTTPException (status_code=400,detail= 'Bu telefon raqam emas' )
    # #     return v




class UserUpdate(UserBase):
    id: int
    password: str
    number: str
    kpi: List[KpiBase]


class UpdateUserBalance(BaseModel):
    id: int
    balance: float
    user_id: int

class UpdateUserSalary(BaseModel):
    id: int
    salary: float
    user_id: int
class UpdateUserSalaryBalance(BaseModel):
    id: int
    balance: int
    salary: int
    user_id: int

class Token(BaseModel):
    access_token = str
    token = str


class TokenData(BaseModel):
    id: Optional[str] = None

class UserCurrent(BaseModel):
    id:int
    name: str
    username: str
    password:str
    roll: str
    status: bool
