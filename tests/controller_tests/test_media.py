from . import helpers


def test_get_upload_url(client, mock_graph, mock_zep_client, mock_generate_otp):
    helpers.get_new_user_and_login(client, scope="")
    response = client.post(
        "media/get-upload-url",
        json=dict(name="test.jpg", format="jpg")
        )
    assert response.status_code == 200
