def test_login_success(client):
    """POST /auth/login with valid credentials returns token."""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["token"] == "mock-jwt-token-12345"
    assert data["message"] == "Login successful"


def test_login_invalid_username(client):
    """POST /auth/login with invalid username returns 401."""
    response = client.post(
        "/auth/login",
        json={"username": "wronguser", "password": "password"},
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_invalid_password(client):
    """POST /auth/login with invalid password returns 401."""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_login_missing_fields(client):
    """POST /auth/login with missing fields returns 422."""
    response = client.post("/auth/login", json={})
    assert response.status_code == 422

    response = client.post("/auth/login", json={"username": "admin"})
    assert response.status_code == 422

    response = client.post("/auth/login", json={"password": "password"})
    assert response.status_code == 422
