from pydantic import BaseModel

class CartItemIn(BaseModel):
    product_id: int
    quantity: int


class CartItemOut(BaseModel):
    product_id: int
    quantity: int
