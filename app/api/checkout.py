from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.models.user import User
from app.services.checkout_service import checkout
from app.schemas.checkout import CheckoutIn
from app.schemas.order import OrderOut
from app.models.order import Order
from app.models.coupon import Coupon
from app.schemas.coupon import CouponOut

router = APIRouter(prefix="/checkout", tags=["Checkout"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}", response_model=OrderOut)
def do_checkout(
    user_id: int,
    payload: CheckoutIn,
    db: Session = Depends(get_db),
):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    return checkout(db, user_id, payload.coupon_code)

@router.get("/orders/{user_id}", response_model=List[OrderOut])
def get_orders(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Order).filter_by(user_id=user_id).all()


@router.get("/coupons/{user_id}", response_model=List[CouponOut])
def get_user_coupons(user_id: int, db: Session = Depends(get_db)):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return db.query(Coupon).filter_by(user_id=user_id).all()
