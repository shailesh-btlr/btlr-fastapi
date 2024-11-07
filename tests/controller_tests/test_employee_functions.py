from . import helpers


def test_create_employee(client, mock_graph, mock_zep_client, mock_generate_otp):
    user = helpers.get_new_user_and_login(
        client, scope="admin")
    business = client.post("businesses", json=dict(name="Btlr")).json()
    employee = client.post("employees", json=dict(
        business_id=business["id"],
        user_id=user["id"])
    ).json()
    assert employee["business_id"] == business["id"]
    assert employee["user_id"] == user["id"]


def test_create_department(client):
    response = client.post("departments", json=dict(
        name="Test Department",
        business_id=1,
        parent_id=None,
    ))
    assert response.status_code == 200
    assert response.json()["name"] == "Test Department"


def test_create_role(client):
    response = client.post("roles", json=dict(
        name="Test Role",
        description="str",
        task_list="str",
        business_id=1
    ))
    assert response.status_code == 200
    assert response.json()["name"] == "Test Role"


def test_create_employee_function(client):
    response = client.post("employee-functions", json=dict(
        employee_id=1,
        role_id=1,
        department_id=1
    ))
    assert response.status_code == 200
    assert response.json()["employee_id"] == 1
    assert response.json()["role_id"] == 1
    assert response.json()["department_id"] == 1


def test_create_duplicate_employee_function(client):
    response = client.post("employee-functions", json=dict(
        employee_id=1,
        role_id=1,
        department_id=1
    ))
    assert response.status_code == 400


def test_read_employee_function(client):
    response = client.get("employee-functions/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_read_nonexistent_employee_function(client):
    response = client.get("employee-functions/999")

    assert response.status_code == 404


def test_get_employee_functions(client):
    response = client.get("/employees/1/functions")

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["employee_id"] == 1
    assert response.json()[0]["role_id"] == 1
    assert response.json()[0]["department_id"] == 1
    assert response.json()[0]["role"]["id"] == 1
    assert response.json()[0]["role"]["name"] == "Test Role"
    assert response.json()[0]["department"]["id"] == 1
    assert response.json()[0]["department"]["name"] == "Test Department"


def test_update_employee_function(client):
    new_role = client.post("roles", json=dict(
        name="Another Test Role",
        description="str",
        task_list="str",
        business_id=1
    )).json()
    response = client.put("employee-functions/1", json=dict(
        employee_id=1,
        role_id=new_role["id"],
        department_id=1
    ))
    assert response.status_code == 200
    assert response.json()["role_id"] == new_role["id"]
    assert response.json()["department_id"] == 1


def test_update_nonexistent_employee_function(client):
    response = client.put("employee-functions/999", json=dict(
        employee_id=1,
        role_id=2,
        department_id=2
    ))
    assert response.status_code == 404


def test_delete_employee_function(client):
    response = client.delete("employee-functions/1")
    assert response.status_code == 200


def test_delete_nonexistent_employee_function(client):
    response = client.delete("employee-functions/999")
    assert response.status_code == 404
