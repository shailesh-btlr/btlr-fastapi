from . import helpers


def test_create_department(client, mock_graph, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, "admin")
    business = client.post("businesses", json=dict(name="B")).json()
    response = client.post(
        "departments",
        json=dict(
            name="TestDepartment", business_id=business["id"], parent_id=None
        ),
    )
    assert response.status_code == 200
    assert response.json()
    assert response.json()["name"] == "TestDepartment"
    assert response.json()["business_id"] == 1
    assert response.json()["parent_id"] is None


def test_update_department(client):
    response = client.put("departments/1", json=dict(name="TestDepartment123"))
    assert response.status_code == 200
    assert response.json()
    assert response.json()["name"] == "TestDepartment123"
    assert response.json()["business_id"] == 1
    assert response.json()["parent_id"] is None
    assert response.json()["id"] == 1


def test_create_child_department(client):
    response = client.post(
        "departments",
        json=dict(name="TestDepartment", business_id=1, parent_id=1),
    )
    assert response.status_code == 200
    assert response.json()
    assert response.json()["name"] == "TestDepartment"
    assert response.json()["business_id"] == 1
    assert response.json()["parent_id"] == 1


def test_read_department(client):
    response = client.get("departments/1")
    assert response.status_code == 200
    assert response.json()
    assert response.json()["id"] == 1


def test_read_nonexistent_department(client):
    response = client.get("departments/999")
    assert response.status_code == 404


def test_list_departments(client):
    response = client.get("departments?business_id=1")
    assert response.status_code == 200
    assert response.json()
    assert isinstance(response.json(), list)


def test_delete_department(client):
    response = client.delete("departments/1")
    assert response.status_code == 200


def test_read_deleted_department(client):
    response = client.get("departments/2")
    assert response.status_code == 404


def test_delete_nonexistent_department(client):
    response = client.delete("departments/999")
    assert response.status_code == 404
