from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.deps import get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_order() -> None:
    response = client.post(
        "/orders",
        json={
            "external_order_id": "TEST-1001",
            "channel": "shopify",
            "customer_name": "Test Customer",
            "total_amount": "42.50",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["external_order_id"] == "TEST-1001"
    assert data["channel"] == "shopify"
    assert data["customer_name"] == "Test Customer"
    assert data["total_amount"] == "42.50"
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_list_orders() -> None:
    client.post(
        "/orders",
        json={
            "external_order_id": "TEST-2001",
            "channel": "shopify",
            "customer_name": "List Customer",
            "total_amount": "25.00",
        },
    )

    response = client.get("/orders")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_order() -> None:
    create_response = client.post(
        "/orders",
        json={
            "external_order_id": "TEST-3001",
            "channel": "shopify",
            "customer_name": "Get Customer",
            "total_amount": "30.00",
        },
    )

    order_id = create_response.json()["id"]

    response = client.get(f"/orders/{order_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["external_order_id"] == "TEST-3001"


def test_get_order_not_found() -> None:
    response = client.get("/orders/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_update_order_status() -> None:
    create_response = client.post(
        "/orders",
        json={
            "external_order_id": "TEST-4001",
            "channel": "shopify",
            "customer_name": "Status Customer",
            "total_amount": "50.00",
        },
    )

    order_id = create_response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "processing"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == order_id
    assert data["status"] == "processing"


def test_update_order_status_rejects_invalid_status() -> None:
    create_response = client.post(
        "/orders",
        json={
            "external_order_id": "TEST-5001",
            "channel": "shopify",
            "customer_name": "Invalid Status Customer",
            "total_amount": "60.00",
        },
    )

    order_id = create_response.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        json={"status": "invalid"},
    )

    assert response.status_code == 422
