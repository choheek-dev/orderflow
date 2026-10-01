from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.orders import router as orders_router

app = FastAPI(
    title="OrderFlow API",
    description="Backend API for the OrderFlow order management platform",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(orders_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "OrderFlow API is running"}
