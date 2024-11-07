def test_create_user(client, mock_graph, mock_zep_client, mock_request):
    response = client.post(
        "users",
        json=dict(
            email="Test@example.com"
        ),
    )
    assert response.status_code == 200
    assert response.json()["email"] == "Test@example.com"
    mock_request.assert_called_once_with(
        "GET",
        "https://chat.btlr.vip/api/register?user=1&host=chat.btlr.vip&password=btlrbtlr",
        auth=("admin@chat.btlr.vip", "password"),
    )


def test_create_duplicate_user(client):
    response = client.post(
        "users",
        json=dict(
            email="test@example.com"
        ),
    )
    assert response.status_code == 400


def test_search_user_by_email(client):
    response = client.get("/users?email=test@example.com")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "Test@example.com"


def test_search_user_by_nonexistent_email(client):
    response = client.get("/users?email=nonexistent@example.com")
    assert response.status_code == 200
    assert response.json() == []


def test_read_user(client):
    response = client.get("users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_read_nonexistent_user(client):
    response = client.get("users/999")
    assert response.status_code == 404


def test_delete_nonexistent_user(client):
    response = client.delete("users/999")
    assert response.status_code == 404


def test_delete_user(client):
    response = client.delete("users/1")
    assert response.status_code == 200
