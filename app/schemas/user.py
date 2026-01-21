from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
