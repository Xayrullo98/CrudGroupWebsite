from pydantic import BaseModel


class ExtraWorksBase(BaseModel):
    work: str


class ExtraWorksCreate(ExtraWorksBase):
    pass


class ExtraWorksUpdate(ExtraWorksBase):
    id: int
    status: bool = True
    
