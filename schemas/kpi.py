from pydantic import BaseModel


class KpiBase(BaseModel):
	percentage: float
	


class KpiCreate(KpiBase):
	source_id: int
	


class KpiUpdate(KpiBase):
	id: int
	source_id: int
	status: bool
