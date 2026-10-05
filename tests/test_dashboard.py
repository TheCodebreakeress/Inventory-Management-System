from tests import client, reset_database  # noqa: F401


def test_dashboard_statistics(client):
    """Test dashboard aggregation metrics."""
    # Check empty dashboard
    res_empty = client.get("/api/dashboard")
    assert res_empty.status_code == 200
    assert res_empty.json() == {
        "total_products": 0,
        "total_suppliers": 0,
        "total_stock": 0,
        "low_stock_products": 0,
        "total_stock_in_transactions": 0,
        "total_stock_out_transactions": 0,
    }

    # Create 2 suppliers
    client.post(
        "/api/suppliers",
        json={"name": "Sup 1", "email": "s1@test.com", "phone": "111"},
    )
    client.post(
        "/api/suppliers",
        json={"name": "Sup 2", "email": "s2@test.com", "phone": "222"},
    )

    # Create 3 products
    p1 = client.post(
        "/api/products",
        json={"name": "Prod 1", "sku": "D-001", "category": "A", "price": 10.0, "quantity": 5},
    ).json()["id"]

    p2 = client.post(
        "/api/products",
        json={"name": "Prod 2", "sku": "D-002", "category": "B", "price": 20.0, "quantity": 15},
    ).json()["id"]

    p3 = client.post(
        "/api/products",
        json={"name": "Prod 3", "sku": "D-003", "category": "C", "price": 30.0, "quantity": 4},
    ).json()["id"]

    # At this point:
    # total_products: 3, total_suppliers: 2
    # total_stock: 5 + 15 + 4 = 24
    # low_stock_products: p1 (5) and p3 (4) -> 2 (< threshold 10)

    # Perform Stock IN transactions
    client.post("/api/stock/in", json={"product_id": p1, "quantity": 10})  # p1 now 15
    client.post("/api/stock/in", json={"product_id": p2, "quantity": 5})   # p2 now 20

    # Perform Stock OUT transaction
    client.post("/api/stock/out", json={"product_id": p2, "quantity": 4})  # p2 now 16

    # Current state:
    # p1: 15
    # p2: 16
    # p3: 4
    # total_stock: 15 + 16 + 4 = 35
    # low_stock_products: p3 (4 < 10) -> 1
    # total_stock_in_transactions: 2
    # total_stock_out_transactions: 1

    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] == 3
    assert data["total_suppliers"] == 2
    assert data["total_stock"] == 35
    assert data["low_stock_products"] == 1
    assert data["total_stock_in_transactions"] == 2
    assert data["total_stock_out_transactions"] == 1
