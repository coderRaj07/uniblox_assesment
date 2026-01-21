from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import SessionLocal
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemIn, CartItemOut

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}/add", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    user_id: int,
    item: CartItemIn,
    db: Session = Depends(get_db)
):
    #  Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Check if item already exists in cart
    cart_item = (
        db.query(CartItem)
        .filter(
            CartItem.user_id == user_id,
            CartItem.product_id == item.product_id
        )
        .first()
    )

    if cart_item:
        # Update quantity if already present
        cart_item.quantity += item.quantity
    else:
        # Add new cart item
        cart_item = CartItem(
            user_id=user_id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return {
        "message": "Item added to cart",
        "cart_item": {
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }
    }

@router.get("/{user_id}", response_model=List[CartItemOut])
def view_cart(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return db.query(CartItem).filter_by(user_id=user_id).all()
