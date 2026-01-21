from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String)
    user_id = Column(Integer)
    generated_at_order = Column(Integer)
    is_used = Column(Boolean, default=False)
