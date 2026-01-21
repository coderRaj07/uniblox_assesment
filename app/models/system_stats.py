from sqlalchemy import Column, Integer
from app.core.database import Base

class SystemStats(Base):
    __tablename__ = "system_stats"
    id = Column(Integer, primary_key=True)
    total_orders = Column(Integer)
