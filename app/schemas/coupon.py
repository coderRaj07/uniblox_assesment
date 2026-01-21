from pydantic import BaseModel

class CouponOut(BaseModel):
    code: str
    is_used: bool
    generated_at_order: int

    class Config:
        from_attributes = True
