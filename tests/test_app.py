import sys
import os

# Add backend directory to Python path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "backend")
    )
)

from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200


def test_get_menu():
    client = app.test_client()

    response = client.get("/api/menu")

    assert response.status_code == 200


def test_get_orders():
    client = app.test_client()

    response = client.get("/api/orders")

    assert response.status_code == 200


def test_invalid_order():
    client = app.test_client()

    response = client.post(
        "/api/order",
        json={}
    )

    assert response.status_code == 400