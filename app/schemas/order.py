from pydantic import BaseModel
from typing import Optional

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    discount_amount: float
    final_amount: float
    coupon_code: Optional[str]

    class Config:
        from_attributes = True
