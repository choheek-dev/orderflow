from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead, OrderStatusUpdate

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[OrderRead])
def list_orders(db: DbSession) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: DbSession) -> Order:
    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    return order


@router.post(
    "",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
)
def create_order(order_data: OrderCreate, db: DbSession) -> Order:
    order = Order(
        external_order_id=order_data.external_order_id,
        channel=order_data.channel,
        customer_name=order_data.customer_name,
        total_amount=order_data.total_amount,
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    db: DbSession,
) -> Order:
    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order
