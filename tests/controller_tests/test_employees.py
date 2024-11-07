from . import helpers


def test_create_employee(client, mock_graph, mock_zep_client, mock_generate_otp):
    user = helpers.get_new_user_and_login(client, scope="business admin")
    business = client.post("businesses", json=dict(name="Btlr")).json()
    employee = client.post(
        "employees", json=dict(business_id=business["id"], user_id=user["id"])
    ).json()
    assert employee["business_id"] == business["id"]
    assert employee["user_id"] == user["id"]


def test_create_duplicate_employee(client):
    response = client.post("employees", json=dict(business_id=1, user_id=1))
    assert response.status_code == 400


def test_get_employees(client):
    response = client.get("employees?business_id=1")
    assert response.status_code == 200
    assert response.json()[0]["business_id"] == 1
    assert response.json()[0]["user_id"] == 1
    assert response.json()[0]["user"]["email"] == "a@b.c"


def test_get_nonexistent_employee(client):
    response = client.get("employees?business_id=999")
    assert response.status_code == 200
    assert response.json() == []


def test_delete_employee(client):
    response = client.delete("employees/1")
    assert response.status_code == 200


def test_delete_nonexistent_employee(client):
    response = client.delete("employees/999")
    assert response.status_code == 404
