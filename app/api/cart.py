from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.cart import CartItem
from app.schemas.cart import CartItemIn, CartItemOut

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}/add")
def add_to_cart(
    user_id: int,
    item: CartItemIn,
    db: Session = Depends(get_db)
):
    cart_item = CartItem(
        user_id=user_id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(cart_item)
    db.commit()
    return {"message": "Item added to cart"}

@router.get("/{user_id}", response_model=List[CartItemOut])
def view_cart(user_id: int, db: Session = Depends(get_db)):
    items = db.query(CartItem).filter_by(user_id=user_id).all()
    return items
