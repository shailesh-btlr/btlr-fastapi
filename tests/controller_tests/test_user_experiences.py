from fastapi import status

from .helpers import get_new_user_and_login


def test_check_in(client, mock_graph, mock_request, mock_zep_client, mock_generate_otp):
    user = get_new_user_and_login(client, "admin")
    business = client.post("businesses", json=dict(name="B")).json()
    response = client.post(
        "experiences/check-in",
        json=dict(user_id=user["id"], business_id=business["id"]),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert len(response_data) == 9
    assert response_data["id"] == 1
    assert response_data["business_id"] == 1
    assert response_data["user_id"] == 1
    assert response_data["state"] == "idle"
    assert response_data["assigned_department_id"] is None
    assert response_data["assigned_role_id"] is None
    assert response_data["assigned_user_id"] is None
    assert response_data["created_at"] is not None
    assert response_data["updated_at"] is not None


def test_experience_diagram(client):
    response = client.get("experiences/1/diagram.svg")

    assert response.status_code == status.HTTP_200_OK
    assert response.content.startswith(b"<?xml")
    assert response.headers["content-type"] == "image/svg+xml"


def test_disallow_second_check_in_while_not_checked_out(client):
    response = client.post(
        "experiences/check-in",
        json=dict(user_id=1, business_id=1),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "details": "User experience 1 is already in progress."
    }


def test_check_in_user_unknown_error(client):
    response = client.post(
        "experiences/check-in",
        json=dict(user_id="101", business_id="102"),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"details": "User 101 not found."}


def test_check_in_business_unknown_error(client):
    response = client.post(
        "experiences/check-in",
        json=dict(user_id="1", business_id="102"),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"details": "Business 102 not found."}


def test_get_experience(client):
    response = client.get("experiences/1")

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["business_id"] == 1
    assert response_data["user_id"] == 1
    assert response_data["state"] == "idle"
    assert response_data["created_at"] is not None
    assert response_data["updated_at"] is not None


def test_get_experiences(client):
    response = client.get(
        "experiences?user_id=1&business_id=1&state=idle",
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert len(response_data) == 1
    assert response_data[0]["id"] == 1
    assert response_data[0]["business_id"] == 1
    assert response_data[0]["user_id"] == 1
    assert response_data[0]["state"] == "idle"
    assert response_data[0]["created_at"] is not None
    assert response_data[0]["updated_at"] is not None


def test_assign_experience(client):
    department = client.post(
        "departments",
        json=dict(name="TestDepartment", business_id=1, parent_id=None),
    ).json()
    role = client.post(
        "roles",
        json=dict(
            name="Test Role",
            description="Test Role",
            task_list="Test Role",
            parent_id=None,
            business_id=1,
        ),
    ).json()
    response = client.put(
        "experiences/1/assign",
        json=dict(
            department_id=department["id"], role_id=role["id"], user_id=1
        ),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "assigned"
    assert response_data["assigned_department_id"] == department["id"]
    assert response_data["assigned_role_id"] == role["id"]
    assert response_data["assigned_user_id"] == 1


def test_invalid_state_transition(client):
    response = client.put(
        "experiences/1/assign",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_accept_assigment(client):
    response = client.put(
        "experiences/1/accept",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "owned"


def test_reassign_experience(client):
    response = client.put(
        "experiences/1/assign",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "assigned"


def test_decline_assignment(client):
    response = client.put(
        "experiences/1/decline",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "idle"


def test_unassign(client):
    client.put(
        "experiences/1/assign",
        json=dict(department_id=1, role_id=1, user_id=1),
    )
    client.put(
        "experiences/1/accept",
        json=dict(department_id=1, role_id=1, user_id=1),
    )
    response = client.put(
        "experiences/1/unassign",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "idle"
    assert response_data["assigned_department_id"] is None
    assert response_data["assigned_role_id"] is None
    assert response_data["assigned_user_id"] is None


def test_check_out(client):
    client.put(
        "experiences/1/assign",
        json=dict(department_id=1, role_id=1, user_id=1),
    )
    client.put(
        "experiences/1/accept",
        json=dict(department_id=1, role_id=1, user_id=1),
    )
    response = client.put(
        "experiences/1/check-out",
        json=dict(department_id=1, role_id=1, user_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["state"] == "checked_out"


def test_allow_second_check_in_after_checkout(client):
    response = client.post(
        "experiences/check-in",
        json=dict(user_id=1, business_id=1),
    )

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert response_data["id"] == 2
    assert response_data["state"] == "idle"
