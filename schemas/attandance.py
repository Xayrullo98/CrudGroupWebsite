from enum import Enum
from pydantic import BaseModel
from pydantic.datetime_parse import  datetime
from typing import Optional, List


class NewAttandance(BaseModel):

    user_id: int
    authorizator: str


class AttType(str, Enum):
    entry="entry"
    exit="exit"

class AttTypeHik(str, Enum):
    entry="checkIn"
    exit="checkOut"


class UpdateAttandance(BaseModel):
    type: str
    user_id: int
    working_period: datetime
    authorizator: str
    datetime: str

class AccessControllerEvent(BaseModel):
    deviceName: str
    name: str
    employeeNoString: str
    attendanceStatus: AttTypeHik

class EventLogItem(BaseModel):
    dateTime: str
    deviceID: str
    AccessControllerEvent: AccessControllerEvent

class EventLog(BaseModel):
    event_log: List[EventLogItem]