from . import helpers


def test_create_business(
        client, mock_graph, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, scope="admin")
    response = client.post("businesses", json=dict(name="TestBusiness"))
    assert response.status_code == 200


def test_fail_on_create_duplicate(client):
    # this runs after test_01
    response = client.post("businesses", json=dict(name="TestBusiness"))
    assert response.status_code == 400


def test_get_business(client):
    response = client.get("businesses/1")
    assert response.json() == dict(id=1, name="TestBusiness", prompt=None)


def test_get_unknown_business(client):
    response = client.get("businesses/999")
    assert response.status_code == 404


def test_update_business(client):
    response = client.put("businesses/1", json=dict(name="T", prompt="gpt"))
    assert response.json() == dict(id=1, name="T", prompt="gpt")
