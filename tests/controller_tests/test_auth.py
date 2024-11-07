import pytest
from fastapi import status
from unittest.mock import ANY 


def test_create_user_success(
        client, mock_graph, mock_zep_client, mock_generate_otp):
    response = client.post(
        "users",
        json=dict(email="test@example.com"),
    )
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "id" in response_data
    assert response_data["email"] == "test@example.com"


def test_request_otp(client, mock_generate_otp, mock_send_otp_email):
    response = client.post(
        "auth/request-otp",
        json=dict(email="test@example.com")
    )
    assert response.status_code == status.HTTP_200_OK
    mock_send_otp_email.assert_called_once_with(ANY, "test@example.com")
    mock_generate_otp.assert_called_once()


def test_request_otp_invalid_email(client, mock_send_otp_email):
    response = client.post(
        "auth/request-otp",
        json=dict(email="invalid@example.com")
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    mock_send_otp_email.assert_not_called()


def test_login_user_success(client, mock_generate_otp):
    login_data = {
        "username": "test@example.com",
        "password": "00000",
        "scope": "",
    }
    response = client.post("auth", data=login_data)

    response_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data["access_token"] is not None


def test_login_user_user_not_found(client):
    login_data = {
        "username": "invalid@example.com",
        "password": "password",
        "scope": "",
    }
    response = client.post("auth", data=login_data)

    response_data = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data["detail"] == "Incorrect username or password"


def test_login_user_invalid_credentials(client):
    response = client.post(
        "auth",
        data={
            "username": "test@example.com",
            "password": "wrong_password",
            "scope": "",
        },
    )

    response_data = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_data["detail"] == "Incorrect username or password"


def test_refresh_token(client, mock_generate_otp):
    login_response = client.post(
        "auth",
        data={
            "username": "test@example.com",
            "password": "00000",
            "scope": "",
        },
    )
    login_response_data = login_response.json()
    assert login_response.status_code == status.HTTP_200_OK
    assert login_response_data["access_token"].startswith("ey")
    assert login_response_data["refresh_token"].startswith("ey")

    refresh_response = client.post(
        "auth/refresh", data={"token": login_response_data["refresh_token"]}
    )
    refresh_response_data = refresh_response.json()
    assert refresh_response.status_code == status.HTTP_200_OK
    assert refresh_response_data["access_token"].startswith("ey")
    assert refresh_response_data["refresh_token"].startswith("ey")
    assert (
        refresh_response_data["refresh_token"]
        != login_response_data["refresh_token"]
    )
