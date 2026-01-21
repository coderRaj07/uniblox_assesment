from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.database import engine, Base, SessionLocal
from app.core.seed import seed_data
from app.api import user, product, cart, checkout, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup logic ----
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    yield

    # ---- Shutdown logic (optional) ----
    # Nothing to clean up for in-memory DB


app = FastAPI(
    title="UniBlox – Nth Order Coupon Simulator",
    lifespan=lifespan
)

# Routers
app.include_router(user.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(checkout.router)
app.include_router(admin.router)
