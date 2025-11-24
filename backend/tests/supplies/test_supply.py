import pytest
from fastapi import HTTPException
from uuid import UUID

from app.schemas.supply import SupplyCreate, SupplyUpdate

def test_create_supply(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    
    data = {
        "name": "Test Supply",
        "unit": "kg",
        "cost_per_unit": 10.5,
        "stock_quantity": 100.0,
        "min_stock": 10.0

    }
    
    response = client.post("/api/v1/supplies/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Supply"

def test_get_supplies(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.get("/api/v1/supplies/", headers=headers)
    assert response.status_code == 200

    result = response.json()
    assert isinstance(result, list)

def test_get_supply(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    data = {
        "name": "Feijão",
        "unit": "kg",
        "stock_quantity": 8,
        "cost_per_unit": 4.50,
        "category": "Ingredientes",
        "min_stock": 2.0
    }

    create = client.post("/api/v1/supplies/", json=data, headers=headers)
    supply_id = create.json()["id"]

    response = client.get(f"/api/v1/supplies/{supply_id}", headers=headers)
    assert response.status_code == 200

    result = response.json()
    assert result["id"] == supply_id
    assert result["name"] == "Feijão"

def test_update_supply(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    data = {
        "name": "Óleo de cozinha",
        "unit": "l",
        "stock_quantity": 5,
        "cost_per_unit": 7.50,
        "category": "Ingredientes",
        "min_stock": 2.0
    }
    created = client.post("/api/v1/supplies/", json=data, headers=headers)
    supply_id = created.json()["id"]

    update_data = {"stock_quantity": 10}

    response = client.patch(
        f"/api/v1/supplies/{supply_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200

    result = response.json()
    assert result["stock_quantity"] == 10

def test_delete_supply(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    data = {
        "name": "Açúcar",
        "unit": "kg",
        "stock_quantity": 15,
        "cost_per_unit": 2.20,
        "category": "Ingredientes",
        "min_stock": 5.0
    }
    created = client.post("/api/v1/supplies/", json=data, headers=headers)
    supply_id = created.json()["id"]

    response = client.delete(f"/api/v1/supplies/{supply_id}", headers=headers)
    assert response.status_code == 200

    response2 = client.get(f"/api/v1/supplies/{supply_id}", headers=headers)
    assert response2.status_code == 404

def test_create_supply_missing_name(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    data = {
        "unit": "kg",
        "cost_per_unit": 5.0,
        "stock_quantity": 10.0,
        "min_stock": 2.0
    }

    response = client.post("/api/v1/supplies/", json=data, headers=headers)
    assert response.status_code == 422

def test_create_supply_invalid_type_cost(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.post(
        "/api/v1/supplies/",
        json={
            "name": "Rice",
            "unit": "kg",
            "cost_per_unit": "NOT_A_NUMBER",
            "stock_quantity": 10,
            "min_stock": 2
        },
        headers=headers
    )
    assert response.status_code == 422

def test_create_supply_negative_stock(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.post(
        "/api/v1/supplies/",
        json={
            "name": "Salt",
            "unit": "kg",
            "cost_per_unit": 1.22,
            "stock_quantity": -5,
            "min_stock": 1,
        },
        headers=headers
    )
    assert response.status_code == 422

def test_create_supply_min_stock_greater_than_stock(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.post(
        "/api/v1/supplies/",
        json={
            "name": "Flour",
            "unit": "kg",
            "cost_per_unit": 3.50,
            "stock_quantity": 2,
            "min_stock": 10,
        },
        headers=headers
    )
    assert response.status_code in (400, 422)

def test_get_supply_invalid_uuid(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.get("/api/v1/supplies/not-a-uuid", headers=headers)
    assert response.status_code == 422


def test_get_supply_not_found(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    import uuid
    fake_id = str(uuid.uuid4())

    response = client.get(f"/api/v1/supplies/{fake_id}", headers=headers)
    assert response.status_code == 404

def test_update_supply_not_found(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    import uuid
    fake_id = str(uuid.uuid4())

    response = client.patch(
        f"/api/v1/supplies/{fake_id}",
        json={"stock_quantity": 99},
        headers=headers
    )
    assert response.status_code == 404

def test_update_supply_invalid_value_type(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    # First create
    create = client.post(
        "/api/v1/supplies/",
        json={
            "name": "Coffee",
            "unit": "kg",
            "stock_quantity": 50,
            "cost_per_unit": 7.5,
            "min_stock": 5
        },
        headers=headers
    )
    supply_id = create.json()["id"]

    # Try invalid update
    response = client.patch(
        f"/api/v1/supplies/{supply_id}",
        json={"stock_quantity": "invalid"},
        headers=headers
    )
    assert response.status_code == 422

def test_delete_supply_invalid_uuid(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    response = client.delete("/api/v1/supplies/invalid-uuid", headers=headers)
    assert response.status_code == 422

def test_delete_supply_not_found(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}

    import uuid
    fake_id = str(uuid.uuid4())

    response = client.delete(f"/api/v1/supplies/{fake_id}", headers=headers)
    assert response.status_code == 404

def test_create_supply_no_token(client):
    with pytest.raises(HTTPException) as exc_info:
        client.post(
            "/api/v1/supplies/",
            json={
                "name": "Test",
                "unit": "kg",
                "stock_quantity": 10,
                "cost_per_unit": 1,
                "min_stock": 1
            }
        )
    assert exc_info.value.status_code == 401
