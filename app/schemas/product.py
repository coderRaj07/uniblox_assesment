from pydantic import BaseModel

class ProductOut(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True
