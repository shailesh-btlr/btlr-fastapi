from . import helpers


def test_create_touchpoint(client, mock_graph, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, scope="admin")
    business = client.post("businesses", json=dict(name="Btlr")).json()
    department = client.post("departments", json=dict(
        name="TestDepartment",
        business_id=business["id"],
        parent_id=None)
    ).json()
    touchpoint_dict = dict(
        name="TestTouchpoint",
        description="TestDescription",
        business_id=business["id"],
        department_id=department["id"]
    )
    response = client.post("touchpoints", json=touchpoint_dict)
    touchpoint = response.json()
    assert response.status_code == 201
    assert touchpoint["id"] is not None
    assert touchpoint["name"] == touchpoint_dict["name"]
    assert touchpoint["description"] == touchpoint_dict["description"]
    assert touchpoint["department"]["name"] == department["name"]


def test_read_touchpoint(client):
    response = client.get("touchpoints/1")
    touchpoint = response.json()
    assert response.status_code == 200
    assert touchpoint["name"] == "TestTouchpoint"
    assert touchpoint["description"] == "TestDescription"
    assert touchpoint["department"]["name"] == "TestDepartment"
    assert touchpoint["business"]["name"] == "Btlr"


def test_read_all(client):
    response = client.get("touchpoints?business_id=1")
    assert response.status_code == 200


def test_update(client):
    response = client.put("touchpoints/1", json=dict(
        name="UpdatedTouchpoint",
        description="TestDescription",
        business_id=1,
        department_id=1)
    )
    assert response.status_code == 200


def test_create_touchpoint_cluster(client):
    response = client.post("touchpoints/1/clusters", json=dict(
        name="Wellness")
    )
    assert response.status_code == 201


def test_delete_touchpoint_cluster(client):
    response = client.delete("touchpoints/1/clusters/1")
    assert response.status_code == 204


def test_create_touchpoint_role(client):
    role = client.post("roles", json=dict(
        name="TestRole",
        description="TestDescription",
        task_list="Task1,Task2",
        parent_id=None,
        business_id=1
    )).json()
    response = client.post("touchpoints/1/roles", json=dict(
        role_id=role["id"],
        prompt="GPT")
    )
    touchpoint_role = response.json()
    assert response.status_code == 201
    assert touchpoint_role["role"]["name"] == "TestRole"


def test_update_touchpoint_role(client):
    response = client.put("touchpoints/1/roles/1", json=dict(
        role_id=1,
        prompt="BARD")
    )
    touchpoint_role = response.json()
    assert response.status_code == 200
    assert touchpoint_role["prompt"] == "BARD"


def test_delete_touchpoint_role(client):
    response = client.delete("touchpoints/1/roles/1")
    assert response.status_code == 204


def test_delete_nonexistent_touchpoint_role(client):
    response = client.delete("touchpoints/1/roles/1")
    assert response.status_code == 404


def test_delete_touchpoint_with_cascades(client):
    role = client.post("touchpoints/1/roles", json=dict(
        role_id=1,
        prompt="GPT"
    )).json()
    cluster = client.post("touchpoints/1/clusters", json=dict(
        name="Wellness")
    ).json()
    assert client.delete(
        "touchpoints/1").status_code == 204
    assert client.delete(
        f"touchpoints/1/roles/{role['id']}").status_code == 404
    assert client.delete(
        f"touchpoints/1/clusters/{cluster['id']}").status_code == 404


def test_delete_nonexistent_touchpoint(client):
    assert client.delete("touchpoints/1").status_code == 404
