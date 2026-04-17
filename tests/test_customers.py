def test_get_customers_empty(client):
    response = client.get("/customers/")
    assert response.status_code == 404


def test_create_customer(client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "0412345678"
    }

    response = client.post("/customers/", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["first_name"] == "John"


def test_get_customers_after_create(client):
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "0499999999"
    }

    client.post("/customers/", json=payload)

    response = client.get("/customers/")
    assert response.status_code == 200