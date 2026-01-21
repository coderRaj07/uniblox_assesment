from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.order import Order
from app.models.coupon import Coupon
from app.core.config import NTH_ORDER
from app.models.system_stats import SystemStats
from app.services.coupon_service import (
    invalidate_old_coupons,
    generate_coupon,
)


router = APIRouter(prefix="/admin", tags=["Admin"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    coupons = db.query(Coupon).all()

    return {
        "total_orders": len(orders),
        "total_revenue": sum(o.final_amount for o in orders),
        "total_discount": sum(o.discount_amount for o in orders),
        "total_coupons": len(coupons),
        "used_coupons": len([c for c in coupons if c.is_used]),
    }

@router.post("/coupons/generate")
def admin_generate_coupon(db: Session = Depends(get_db)):
    stats = db.query(SystemStats).first()

    if not stats or stats.total_orders == 0:
        raise HTTPException(400, "No orders placed yet")

    if stats.total_orders % NTH_ORDER != 0:
        raise HTTPException(
            400,
            f"Coupon can only be generated on every {NTH_ORDER}th order"
        )

    # Invalidate previous cycle coupons
    invalidate_old_coupons(db, stats.total_orders)

    # Generate coupon for nth-order user
    from app.models.order import Order
    order = (
        db.query(Order)
        .order_by(Order.id.desc())
        .first()
    )

    coupon = generate_coupon(db, order.user_id, stats.total_orders)
    db.commit()

    return {
        "message": "Coupon generated successfully",
        "coupon_code": coupon.code,
        "user_id": coupon.user_id,
    }
