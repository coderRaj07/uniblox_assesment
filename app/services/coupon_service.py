import uuid
from app.models.coupon import Coupon
from app.models.order import Order
from app.core.config import NTH_ORDER

def invalidate_old_coupons(db, current_order):
    db.query(Coupon).filter(
        Coupon.generated_at_order < current_order
    ).update({"is_used": True})

def generate_coupon(db, user_id, current_order):
    code = f"CPN-{uuid.uuid4().hex[:6]}"
    coupon = Coupon(
        code=code,
        user_id=user_id,
        generated_at_order=current_order,
        is_used=False
    )
    db.add(coupon)
    return coupon

def get_nth_order_user(db, nth_order_number: int):
    order = (
        db.query(Order)
        .filter(Order.id == nth_order_number)
        .first()
    )
    return order.user_id if order else None
