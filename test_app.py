"""
Tests for the Inventory API.
Run: pytest test_app.py -v
All OpenFoodFacts calls are mocked, so no internet is needed.
"""
from unittest.mock import patch
import pytest
from app import app


# ---------- Setup ----------

@pytest.fixture
def client():
    """Give each test a fresh Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------- CRUD Tests ----------

def test_get_all_returns_three_items(client):
    """GET /inventory should return our 3 starting items."""
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_get_one_returns_item_by_id(client):
    """GET /inventory/1 should return the item with id 1."""
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_missing_item_returns_404(client):
    """GET /inventory/999 should fail because it doesn't exist."""
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_create_adds_new_item(client):
    """POST /inventory should create and return the new item."""
    response = client.post("/inventory", json={
        "product_name": "Oat Milk",
        "price": 3.99,
        "stock": 20,
    })
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Oat Milk"


def test_create_without_required_fields_returns_400(client):
    """POST /inventory should fail if price or stock is missing."""
    response = client.post("/inventory", json={"product_name": "Bad"})
    assert response.status_code == 400


def test_update_changes_price(client):
    """PATCH /inventory/1 should change the price."""
    response = client.patch("/inventory/1", json={"price": 9.99})
    assert response.status_code == 200
    assert response.get_json()["price"] == 9.99


def test_delete_removes_item(client):
    """DELETE /inventory/2 should remove it, so GET afterwards returns 404."""
    response = client.delete("/inventory/2")
    assert response.status_code == 200
    assert client.get("/inventory/2").status_code == 404


# ---------- OpenFoodFacts Tests (mocked) ----------

def test_search_by_barcode_found(client):
    """Search by barcode should return the product from OpenFoodFacts."""
    fake_product = {"code": "123", "product_name": "Test Milk", "brands": "TestBrand"}

    with patch("app.off_api.product.get", return_value=fake_product):
        response = client.get("/inventory/search?barcode=123")

    assert response.status_code == 200
    assert response.get_json()["product"]["product_name"] == "Test Milk"


def test_search_by_barcode_not_found(client):
    """OpenFoodFacts returns {'status': 0} for unknown barcodes -> we return 404."""
    with patch("app.off_api.product.get", return_value={"status": 0}):
        response = client.get("/inventory/search?barcode=000")

    assert response.status_code == 404


def test_search_by_name_found(client):
    """Search by name should grab the first product from the results list."""
    fake_results = {
        "count": 1,
        "products": [{"code": "555", "product_name": "Peanut Butter"}],
    }

    with patch("app.off_api.product.text_search", return_value=fake_results):
        response = client.get("/inventory/search?name=peanut")

    assert response.status_code == 200
    assert response.get_json()["product"]["product_name"] == "Peanut Butter"


def test_import_adds_product_from_openfoodfacts(client):
    """Import should fetch from OpenFoodFacts and add it to inventory."""
    fake_product = {"code": "999", "product_name": "Imported Item", "brands": "Brand"}

    with patch("app.off_api.product.get", return_value=fake_product):
        response = client.post("/inventory/import", json={
            "barcode": "999",
            "price": 2.0,
            "stock": 5,
        })

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Imported Item"