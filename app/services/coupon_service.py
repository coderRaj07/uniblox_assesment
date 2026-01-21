import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.models.order import Order
from app.core.config import NTH_ORDER

def invalidate_old_coupons(db: Session, current_order: int):
    if current_order <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid order number"
        )

    (
        db.query(Coupon)
        .filter(
            Coupon.generated_at_order < current_order,
            Coupon.is_used == False
        )
        .update(
            {"is_used": True},
            synchronize_session=False
        )
    )


def generate_coupon(db: Session, user_id: int, current_order: int):
    if user_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID"
        )

    if current_order <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid order number"
        )

    # Ensure order exists and belongs to user
    order = (
        db.query(Order)
        .filter(
            Order.id == current_order,
            Order.user_id == user_id
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found for user"
        )

    # Ensure coupon not already generated for this order
    existing_coupon = (
        db.query(Coupon)
        .filter(Coupon.generated_at_order == current_order)
        .first()
    )

    if existing_coupon:
        return existing_coupon  # idempotency

    code = f"CPN-{uuid.uuid4().hex[:6].upper()}"

    coupon = Coupon(
        code=code,
        user_id=user_id,
        generated_at_order=current_order,
        is_used=False
    )

    db.add(coupon)
    return coupon

def get_nth_order_user(db: Session, nth_order_number: int):
    if nth_order_number <= 0:
        raise HTTPException(
            status_code=400,
            detail="nth_order_number must be greater than zero"
        )

    order = (
        db.query(Order)
        .order_by(Order.created_at.asc())
        .offset(nth_order_number - 1)
        .limit(1)
        .first()
    )

    if not order:
        return None

    return order.user_id
