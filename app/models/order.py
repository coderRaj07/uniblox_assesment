from sqlalchemy import Column, Integer, Float, String
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    total_amount = Column(Float)
    discount_amount = Column(Float)
    final_amount = Column(Float)
    coupon_code = Column(String, nullable=True)
