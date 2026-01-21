from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from app.core.database import Base
from sqlalchemy.orm import relationship

class CartItem(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    product = relationship("Product")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="quantity_positive"),
    )
