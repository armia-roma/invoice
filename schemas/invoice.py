from datetime import date
from pydantic import BaseModel


class Invoice(BaseModel):
    date: date
    total: float
    customer_id: str
    purchase_order_id: int

    class Config:
        orm_mode = True
