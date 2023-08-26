from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class UploadBase(BaseModel):
	source_id: int
	source: str
	comment: str


class UploadCreate(UploadBase):
	pass


class UploadUpdate(UploadBase):
	id: int
	status: bool
