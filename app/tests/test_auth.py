def test_register_and_login(client):
    response = client.post("/auth/register", json={"username": "bibliotecaria", "password": "senha-forte-123"})
    assert response.status_code == 201
    assert response.json()["username"] == "bibliotecaria"

    response = client.post(
        "/auth/login",
        data={"username": "bibliotecaria", "password": "senha-forte-123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_wrong_password_fails(client):
    client.post("/auth/register", json={"username": "usuario", "password": "senha-correta"})
    response = client.post("/auth/login", data={"username": "usuario", "password": "senha-errada"})
    assert response.status_code == 401


def test_protected_route_requires_token(client):
    response = client.post("/authors", json={"name": "Machado de Assis"})
    assert response.status_code == 401
