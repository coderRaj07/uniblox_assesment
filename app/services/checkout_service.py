from app.models.cart import CartItem
from app.models.order import Order
from app.models.system_stats import SystemStats
from app.services.coupon_service import generate_coupon, invalidate_old_coupons
from app.core.config import NTH_ORDER, DISCOUNT_PERCENTAGE


def checkout(db, user_id, coupon_code=None):
    # --- Ensure system stats exist ---
    stats = db.query(SystemStats).first()
    if not stats:
        stats = SystemStats(total_orders=0)
        db.add(stats)
        db.flush()

    stats.total_orders += 1
    current_order = stats.total_orders

    # --- Cart validation ---
    cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
    if not cart_items:
        raise Exception("Cart empty")

    total = sum(item.quantity * 100 for item in cart_items)
    discount = 0
    applied_code = None

    # --- Coupon validation ---
    if coupon_code:
        from app.models.coupon import Coupon

        coupon = db.query(Coupon).filter_by(
            code=coupon_code,
            user_id=user_id,
            is_used=False
        ).first()

        if not coupon or coupon.generated_at_order < current_order - NTH_ORDER:
            raise Exception("Invalid coupon")

        discount = total * DISCOUNT_PERCENTAGE / 100
        coupon.is_used = True
        applied_code = coupon.code

    # --- Create order ---
    order = Order(
        user_id=user_id,
        total_amount=total,
        discount_amount=discount,
        final_amount=total - discount,
        coupon_code=applied_code
    )
    db.add(order)

    # --- Clear cart ---
    db.query(CartItem).filter_by(user_id=user_id).delete()

    # --- Nth-order logic ---
    if current_order % NTH_ORDER == 0:
        invalidate_old_coupons(db, current_order)
        generate_coupon(db, user_id, current_order)

    db.commit()
    return order
