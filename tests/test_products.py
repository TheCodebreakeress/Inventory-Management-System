from tests import client, reset_database  # noqa: F401


def test_create_product(client):
    """Test creating a valid product."""
    # First create a supplier
    sup_res = client.post(
        "/api/suppliers",
        json={"name": "Logitech", "email": "contact@logitech.com", "phone": "1234567890"},
    )
    supplier_id = sup_res.json()["id"]

    payload = {
        "name": "Wireless Mouse",
        "sku": "WM-1001",
        "category": "Electronics",
        "description": "Ergonomic 2.4GHz wireless mouse",
        "price": 29.99,
        "quantity": 50,
        "supplier_id": supplier_id,
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["sku"] == payload["sku"]
    assert data["category"] == payload["category"]
    assert data["price"] == payload["price"]
    assert data["quantity"] == payload["quantity"]
    assert data["supplier_id"] == supplier_id
    assert "created_at" in data
    assert "updated_at" in data


def test_create_product_with_invalid_supplier(client):
    """Test creating a product with non-existent supplier_id fails with 400."""
    payload = {
        "name": "Mechanical Keyboard",
        "sku": "KB-2002",
        "category": "Electronics",
        "price": 89.99,
        "quantity": 15,
        "supplier_id": 9999,
    }
    response = client.post("/api/products", json=payload)
    assert response.status_code == 400
    assert "supplier" in response.json()["detail"].lower()


def test_duplicate_sku(client):
    """Test that creating a product with an existing SKU returns 409 Conflict."""
    payload = {
        "name": "USB-C Cable",
        "sku": "CABLE-001",
        "category": "Accessories",
        "price": 9.99,
        "quantity": 100,
    }
    # First creation should succeed
    res1 = client.post("/api/products", json=payload)
    assert res1.status_code == 201

    # Second creation with identical SKU must fail with 409
    res2 = client.post(
        "/api/products",
        json={
            "name": "Another Cable",
            "sku": "CABLE-001",
            "category": "Accessories",
            "price": 14.99,
            "quantity": 20,
        },
    )
    assert res2.status_code == 409
    assert "already exists" in res2.json()["detail"].lower()


def test_list_products(client):
    """Test listing all products."""
    client.post(
        "/api/products",
        json={"name": "P1", "sku": "SKU-1", "category": "General", "price": 10.0, "quantity": 5},
    )
    client.post(
        "/api/products",
        json={"name": "P2", "sku": "SKU-2", "category": "General", "price": 20.0, "quantity": 10},
    )

    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    skus = [p["sku"] for p in data]
    assert "SKU-1" in skus
    assert "SKU-2" in skus


def test_get_product(client):
    """Test retrieving a single product by ID and 404 for missing product."""
    create_res = client.post(
        "/api/products",
        json={"name": "Monitor", "sku": "MON-4K", "category": "Displays", "price": 299.99, "quantity": 8},
    )
    product_id = create_res.json()["id"]

    # Success
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor"

    # Not found
    not_found_res = client.get("/api/products/9999")
    assert not_found_res.status_code == 404


def test_update_product(client):
    """Test updating product fields and SKU conflict validation."""
    p1 = client.post(
        "/api/products",
        json={"name": "Product 1", "sku": "SKU-AAA", "category": "General", "price": 5.0, "quantity": 10},
    ).json()
    p2 = client.post(
        "/api/products",
        json={"name": "Product 2", "sku": "SKU-BBB", "category": "General", "price": 15.0, "quantity": 20},
    ).json()

    # Successful update
    update_res = client.put(
        f"/api/products/{p1['id']}",
        json={"name": "Product 1 Updated", "price": 7.50},
    )
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Product 1 Updated"
    assert update_res.json()["price"] == 7.50

    # Conflict on changing SKU to existing one
    conflict_res = client.put(
        f"/api/products/{p1['id']}",
        json={"sku": "SKU-BBB"},
    )
    assert conflict_res.status_code == 409

    # 404 for non-existent product
    not_found_res = client.put("/api/products/9999", json={"name": "Ghost"})
    assert not_found_res.status_code == 404


def test_delete_product(client):
    """Test deleting a product and 404 handling."""
    created = client.post(
        "/api/products",
        json={"name": "To Remove", "sku": "RM-001", "category": "Misc", "price": 1.0, "quantity": 2},
    ).json()
    prod_id = created["id"]

    del_res = client.delete(f"/api/products/{prod_id}")
    assert del_res.status_code == 204

    # Verify deleted
    get_res = client.get(f"/api/products/{prod_id}")
    assert get_res.status_code == 404

    # Delete non-existent
    del_non_existent = client.delete(f"/api/products/{prod_id}")
    assert del_non_existent.status_code == 404
