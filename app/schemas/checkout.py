from pydantic import BaseModel, Field
from typing import Optional

class CheckoutIn(BaseModel):
    coupon_code: Optional[str] = Field(
        default="",
        example=""
    )
