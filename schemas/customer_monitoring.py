from pydantic import BaseModel


class Customer_monitoringBase(BaseModel):
	customer_id:int
	customer_status:str
	monitoring_status:bool


class Customer_monitoringCreate(Customer_monitoringBase):
	pass


class Customer_monitoringUpdate(Customer_monitoringBase):
	id: int
	status: bool = True

