from tests import client


def test_register():
    response = client.post(
        "/auth/register",
        json={"username": "testuser123", "password": "testpassword123"},
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}. Response text: {response.text}"
    assert response.json() == {
        "message": "User registered successfully"
    }, f"Unexpected response: {response.text}"


def test_login():
    response = client.post(
        "/auth/login",
        data={"username": "testuser123", "password": "testpassword123"},
    )
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}. Response text: {response.text}"
    assert (
        "access_token" in response.json()
    ), f"Expected 'access_token' in response, got {response.text}"

    return response.json()["access_token"]


def test_get_user():
    access_token = test_login()
    response = client.get("/auth/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}. Response text: {response.text}"
    assert response.json() == {
        "username": "testuser123"
    }, f"Expected username 'testuser123', got {response.text}"


def test_delete_user():
    access_token = test_login()
    response = client.delete("/auth/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert (
        response.status_code == 200
    ), f"Expected status code 200, got {response.status_code}. Response text: {response.text}"
    assert response.json() == {
        "message": "User deleted successfully"
    }, f"Unexpected response: {response.text}"
