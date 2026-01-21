from pydantic import BaseModel, Field

class CartItemIn(BaseModel):
    product_id: int
    quantity: int = Field(
        gt=0,
        description="Quantity must be greater than zero"
    )

class CartItemOut(BaseModel):
    product_id: int
    quantity: int