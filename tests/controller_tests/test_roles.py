from app.schemas.roles import RoleCreate, RoleUpdate
from . import helpers


def test_create_role(client, mock_graph, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, scope="admin")
    business = client.post("businesses", json=dict(name="Btlr")).json()
    role_data = RoleCreate(
        name="Test Role",
        description="Test Role",
        task_list="Test Role",
        parent_id=None,
        business_id=business["id"],
    )
    response = client.post("roles", json=role_data.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "Test Role"
    assert response.json()["description"] == "Test Role"
    assert response.json()["task_list"] == "Test Role"
    assert response.json()["parent_id"] is None
    assert response.json()["business_id"] == business["id"]


def test_create_child_role(client, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, scope="admin")
    role_data = RoleCreate(
        name="Test Child Role",
        description="Test Child Role",
        task_list="Test Child Role",
        parent_id=1,
        business_id=1,
    )
    response = client.post("roles", json=role_data.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "Test Child Role"
    assert response.json()["description"] == "Test Child Role"
    assert response.json()["task_list"] == "Test Child Role"
    assert response.json()["parent_id"] == 1
    assert response.json()["business_id"] == 1


def test_read_role(client):
    response = client.get("roles/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Role"
    assert response.json()["parent_id"] is None
    assert response.json()["business_id"] == 1


# def test_read_all_roles(client):
#     response = client.get("roles?business_id=1")
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             "name": "Test Role",
#             "description": "Test Role",
#             "task_list": "Test Role",
#             "business_id": 1,
#             "parent_id": None,
#             "id": 1,
#         }
#     ]


def test_read_all_roles(client):
    response = client.get("roles?business_id=1")
    assert response.status_code == 200
    assert isinstance(response.json(), list) and len(response.json()) > 0
    first_record = response.json()[0]
    assert first_record == {
        "name": "Test Role",
        "description": "Test Role",
        "task_list": "Test Role",
        "business_id": 1,
        "parent_id": None,
        "id": 1,
    }


def test_update_role(client):
    role_data = RoleUpdate(
        name="Updated Role",
        description="Updated description",
        task_list="Updated task list",
        parent_id=None,
        business_id=1,
    )
    response = client.put("roles/1", json=role_data.model_dump())
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Role"
    assert response.json()["description"] == "Updated description"
    assert response.json()["task_list"] == "Updated task list"
    assert response.json()["parent_id"] is None
    assert response.json()["business_id"] == 1


def test_delete_role(client):
    response = client.delete("roles/1")
    assert response.status_code == 200


def test_read_deleted_role(client):
    response = client.get("roles/2")
    assert response.status_code == 404


def test_read_nonexistent_role(client):
    response = client.get("roles/999")
    assert response.status_code == 404


def test_update_nonexistent_role(client):
    role_data = RoleUpdate(
        name="Updated Role",
        description="Updated description",
        task_list="Updated task list",
        parent_id=0,
        business_id=0,
    )
    response = client.put("roles/999", json=role_data.model_dump())
    assert response.status_code == 404


def test_delete_nonexistent_role(client):
    response = client.delete("roles/999")
    assert response.status_code == 404
