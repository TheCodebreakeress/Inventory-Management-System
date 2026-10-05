from tests import client, reset_database  # noqa: F401


def test_stock_in(client):
    """Test stock IN increases quantity and logs transaction."""
    prod = client.post(
        "/api/products",
        json={"name": "Widget A", "sku": "WGT-A", "category": "Widgets", "price": 12.0, "quantity": 10},
    ).json()
    prod_id = prod["id"]

    response = client.post("/api/stock/in", json={"product_id": prod_id, "quantity": 15})
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == prod_id
    assert data["transaction_type"] == "IN"
    assert data["quantity"] == 15
    assert data["previous_quantity"] == 10
    assert data["new_quantity"] == 25

    # Check updated product
    prod_updated = client.get(f"/api/products/{prod_id}").json()
    assert prod_updated["quantity"] == 25


def test_stock_out(client):
    """Test stock OUT decreases quantity and logs transaction."""
    prod = client.post(
        "/api/products",
        json={"name": "Widget B", "sku": "WGT-B", "category": "Widgets", "price": 20.0, "quantity": 30},
    ).json()
    prod_id = prod["id"]

    response = client.post("/api/stock/out", json={"product_id": prod_id, "quantity": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == prod_id
    assert data["transaction_type"] == "OUT"
    assert data["quantity"] == 10
    assert data["previous_quantity"] == 30
    assert data["new_quantity"] == 20

    # Check updated product
    prod_updated = client.get(f"/api/products/{prod_id}").json()
    assert prod_updated["quantity"] == 20


def test_prevent_negative_stock(client):
    """Test that requesting more stock than available returns 400 and preserves quantity."""
    prod = client.post(
        "/api/products",
        json={"name": "Widget C", "sku": "WGT-C", "category": "Widgets", "price": 15.0, "quantity": 5},
    ).json()
    prod_id = prod["id"]

    response = client.post("/api/stock/out", json={"product_id": prod_id, "quantity": 10})
    assert response.status_code == 400
    assert "insufficient stock" in response.json()["detail"].lower()

    # Verify quantity has not changed
    prod_check = client.get(f"/api/products/{prod_id}").json()
    assert prod_check["quantity"] == 5


def test_stock_transaction_history(client):
    """Test retrieving transaction history and filtering by product ID."""
    p1 = client.post(
        "/api/products",
        json={"name": "Item 1", "sku": "ITM-1", "category": "Misc", "price": 5.0, "quantity": 10},
    ).json()["id"]
    p2 = client.post(
        "/api/products",
        json={"name": "Item 2", "sku": "ITM-2", "category": "Misc", "price": 8.0, "quantity": 20},
    ).json()["id"]

    client.post("/api/stock/in", json={"product_id": p1, "quantity": 5})
    client.post("/api/stock/out", json={"product_id": p1, "quantity": 3})
    client.post("/api/stock/in", json={"product_id": p2, "quantity": 10})

    # Retrieve all transactions
    all_res = client.get("/api/stock")
    assert all_res.status_code == 200
    assert len(all_res.json()) == 3

    # Retrieve filtered transactions for p1
    filtered_res = client.get(f"/api/stock?product_id={p1}")
    assert filtered_res.status_code == 200
    assert len(filtered_res.json()) == 2
    for tx in filtered_res.json():
        assert tx["product_id"] == p1


def test_low_stock(client):
    """Test retrieving products below the low stock threshold (default: 10)."""
    # Low stock product 1 (qty 3 < 10)
    client.post(
        "/api/products",
        json={"name": "Low Item 1", "sku": "LOW-1", "category": "General", "price": 10.0, "quantity": 3},
    )
    # Low stock product 2 (qty 0 < 10)
    client.post(
        "/api/products",
        json={"name": "Low Item 2", "sku": "LOW-2", "category": "General", "price": 15.0, "quantity": 0},
    )
    # Sufficient stock product (qty 25 >= 10)
    client.post(
        "/api/products",
        json={"name": "Good Item", "sku": "GOOD-1", "category": "General", "price": 25.0, "quantity": 25},
    )

    response = client.get("/api/stock/low")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    low_skus = [p["sku"] for p in data]
    assert "LOW-1" in low_skus
    assert "LOW-2" in low_skus
    assert "GOOD-1" not in low_skus
