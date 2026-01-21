from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.cart import CartItem
from app.models.order import Order
from app.models.system_stats import SystemStats
from app.models.user import User
from app.models.coupon import Coupon
from app.models.product import Product
from app.services.coupon_service import generate_coupon, invalidate_old_coupons
from app.core.config import NTH_ORDER, DISCOUNT_PERCENTAGE

def checkout(db: Session, user_id: int, coupon_code: str | None = None):
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user ID")

    try:
        #  TRANSACTION START
        with db.begin():

            # Validate user
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Lock system stats row (prevents race condition)
            stats = (
                db.query(SystemStats)
                .with_for_update()
                .first()
            )

            if not stats:
                stats = SystemStats(total_orders=0)
                db.add(stats)
                db.flush()

            stats.total_orders += 1
            current_order = stats.total_orders

            # Validate cart
            cart_items = (
                db.query(CartItem)
                .join(Product)
                .filter(CartItem.user_id == user_id)
                .all()
            )

            if not cart_items:
                raise HTTPException(
                    status_code=400,
                    detail="Cart is empty"
                )

            # Calculate total safely
            total = sum(
                item.quantity * item.product.price
                for item in cart_items
            )

            discount = 0
            applied_code = None

            # Coupon validation
            if coupon_code:
                coupon = (
                    db.query(Coupon)
                    .filter(
                        Coupon.code == coupon_code,
                        Coupon.user_id == user_id,
                        Coupon.is_used == False
                    )
                    .with_for_update()
                    .first()
                )

                if not coupon:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid or used coupon"
                    )

                if coupon.generated_at_order + NTH_ORDER < current_order:
                    raise HTTPException(
                        status_code=400,
                        detail="Coupon expired"
                    )

                discount = round(total * DISCOUNT_PERCENTAGE / 100, 2)
                coupon.is_used = True
                applied_code = coupon.code

            # Create order
            order = Order(
                user_id=user_id,
                total_amount=total,
                discount_amount=discount,
                final_amount=total - discount,
                coupon_code=applied_code
            )

            db.add(order)

            # Clear cart
            db.query(CartItem).filter(
                CartItem.user_id == user_id
            ).delete()

            # Nth order logic
            if current_order % NTH_ORDER == 0:
                invalidate_old_coupons(db, current_order)
                generate_coupon(db, user_id, current_order)

        # TRANSACTION COMMIT
        return order

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Checkout failed due to database error"
        )
