def test_get_upload_url(client, mock_graph):
    response = client.post(
        "opa",
        json=dict(
            method="OPTION",
            path=["a", "b"],
            claims=dict(
                sub="1",
                exp=123,
                email=None,
                scopes=[]
            )
        )
    )
    assert response.status_code == 200
    assert response.json()["allow"] is True
