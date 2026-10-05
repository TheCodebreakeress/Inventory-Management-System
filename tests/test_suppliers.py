from tests import client, reset_database  # noqa: F401


def test_create_supplier(client):
    """Test creating a new supplier."""
    payload = {
        "name": "Global Supplies Ltd",
        "email": "contact@globalsupplies.com",
        "phone": "+1-555-0199",
        "address": "123 Industrial Way, New York, NY",
    }
    response = client.post("/api/suppliers", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]
    assert "created_at" in data


def test_list_suppliers(client):
    """Test retrieving list of suppliers."""
    client.post(
        "/api/suppliers",
        json={"name": "Supplier A", "email": "a@example.com", "phone": "111-222"},
    )
    client.post(
        "/api/suppliers",
        json={"name": "Supplier B", "email": "b@example.com", "phone": "333-444"},
    )

    response = client.get("/api/suppliers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [s["name"] for s in data]
    assert "Supplier A" in names
    assert "Supplier B" in names


def test_get_supplier(client):
    """Test retrieving a single supplier by ID and error when not found."""
    create_res = client.post(
        "/api/suppliers",
        json={"name": "Tech Corp", "email": "info@techcorp.com", "phone": "555-9876"},
    )
    supplier_id = create_res.json()["id"]

    # Success case
    response = client.get(f"/api/suppliers/{supplier_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Tech Corp"

    # Not found case
    not_found_res = client.get("/api/suppliers/9999")
    assert not_found_res.status_code == 404
    assert "not found" in not_found_res.json()["detail"].lower()


def test_update_supplier(client):
    """Test updating supplier details and 404 on missing supplier."""
    create_res = client.post(
        "/api/suppliers",
        json={"name": "Old Name", "email": "old@example.com", "phone": "123-456"},
    )
    supplier_id = create_res.json()["id"]

    update_payload = {
        "name": "Updated Supplier",
        "address": "456 Renovated Road",
    }
    response = client.put(f"/api/suppliers/{supplier_id}", json=update_payload)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["name"] == "Updated Supplier"
    assert updated_data["address"] == "456 Renovated Road"
    assert updated_data["email"] == "old@example.com"

    # Update non-existent supplier
    not_found_res = client.put("/api/suppliers/9999", json={"name": "Does Not Exist"})
    assert not_found_res.status_code == 404


def test_delete_supplier(client):
    """Test deleting a supplier and 404 error cases."""
    create_res = client.post(
        "/api/suppliers",
        json={"name": "To Delete", "email": "delete@example.com", "phone": "000-000"},
    )
    supplier_id = create_res.json()["id"]

    # Delete supplier
    delete_res = client.delete(f"/api/suppliers/{supplier_id}")
    assert delete_res.status_code == 204

    # Verify deleted
    get_res = client.get(f"/api/suppliers/{supplier_id}")
    assert get_res.status_code == 404

    # Delete non-existent supplier
    not_found_res = client.delete(f"/api/suppliers/{supplier_id}")
    assert not_found_res.status_code == 404
