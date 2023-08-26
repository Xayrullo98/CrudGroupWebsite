from pydantic import BaseModel
from pydantic.datetime_parse import date

class SocialMediaBase(BaseModel):
    name: str
    link: str



class SocialMediaCreate(SocialMediaBase):
    pass


class SocialMediaUpdate(SocialMediaBase):
    id: int
    status: bool
