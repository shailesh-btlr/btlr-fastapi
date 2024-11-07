def get_new_user_and_login(client, scope):
    user = client.post(
        "users",
        json=dict(email="a@b.c"),
    ).json()

    response = client.post(
        "auth",
        data=dict(
            username="a@b.c",
            password="00000",
            scope=scope,
        ),
    )
    client.headers = dict(
        Authorization=f"Bearer {response.json()['access_token']}"
    )
    return user