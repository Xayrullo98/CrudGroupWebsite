from typing import List

from pydantic import BaseModel
from schemas.phones import PhoneBase
from schemas.social_media import SocialMediaBase
class CustomerBase(BaseModel):
	name: str
	address: str



class CustomerCreate(CustomerBase):
	phones : List[PhoneBase]
	social_medias : List[SocialMediaBase]


class CustomerUpdate(CustomerBase):
	phones: List[PhoneBase]
	social_medias: List[SocialMediaBase]
	id: int
	status: bool

	

class CustomerOut(CustomerBase):
		id: int
		user_id: int
		status: bool
		phones : list = []

		class Config:
			orm_mode = True



