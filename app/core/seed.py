from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product


def seed_data(db: Session):
    """
    Seeds initial users and products for development/testing.
    Safe to run multiple times (idempotent).
    """

    # ---- USERS (10) ----
    if db.query(User).count() == 0:
        users = [
            User(name=f"user{i}")
            for i in range(1, 11)
        ]
        db.add_all(users)
        db.commit()

    # ---- PRODUCTS (10) ----
    if db.query(Product).count() == 0:
        products = [
            Product(name="Health Insurance Basic", price=999),
            Product(name="Health Insurance Premium", price=1999),
            Product(name="Life Insurance Term Plan", price=1499),
            Product(name="Life Insurance Premium Plan", price=2499),
            Product(name="Car Insurance Basic", price=799),
            Product(name="Car Insurance Comprehensive", price=1599),
            Product(name="Bike Insurance Basic", price=499),
            Product(name="Bike Insurance Premium", price=899),
            Product(name="Travel Insurance Domestic", price=599),
            Product(name="Travel Insurance International", price=1299),
        ]
        db.add_all(products)
        db.commit()
