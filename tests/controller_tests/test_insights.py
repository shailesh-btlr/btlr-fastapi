from . import helpers


def test_generate_insight(client, mock_flowise, mock_zep_client, mock_generate_otp):
    user = helpers.get_new_user_and_login(client, "admin")

    business = client.post("businesses", json=dict(
        name="TestBusiness"
    )).json()

    department = client.post("departments", json=dict(
        name="TestDepartment",
        business_id=business["id"],
        parent_id=None
    )).json()

    role = client.post("roles", json=dict(
        name="TestRole",
        description="TestRoleDescription",
        task_list="TestRoleTaskList",
        parent_id=None,
        business_id=business["id"]
    )).json()

    touchpoint = client.post("touchpoints", json=dict(
        name="TestTouchpoint",
        description="TestTouchpointDescription",
        business_id=business["id"],
        department_id=department["id"]
    )).json()

    client.post(f"touchpoints/{touchpoint['id']}/roles", json=dict(
        role_id=role["id"],
        prompt="not used"
    ))

    client.post(f"touchpoints/{touchpoint['id']}/clusters", json=dict(
        name="wellness"
        )
    )

    response = client.get(
        f"insights?user_id={user['id']}&"
        f"touchpoint_id={touchpoint['id']}&"
        f"role_id={role['id']}&"
        f"max_tokens=100"
    )

    EXPECTED_PROMPT = (
        f"Touchpoint: {touchpoint['name']} "
        f"Description: {touchpoint['description']} "
        f"Department: {department['name']} "
        f"Service Role: {role['name']} "
        f"Preference theme: wellness "
    )

    insight = response.json()

    mock_flowise.assert_called_once()

    assert response.status_code == 200
    assert insight["prompt"] == EXPECTED_PROMPT
    assert insight["recommendation"] == "MockFlowise"
    assert insight["task_list"] == role["task_list"]
