import os
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

import pytest
from fastapi.testclient import TestClient


class MockNeo4jException(Exception):
    pass


@pytest.fixture(scope="module")
def client():
    from app.config import settings

    settings.SQLALCHEMY_DATABASE_URI = settings.TEST_SQLALCHEMY_DATABASE_URI

    import importlib
    import sys

    from app.main import app

    importlib.reload(sys.modules["app.database"])
    importlib.reload(sys.modules["app.models"])

    yield TestClient(app)

    url = urlparse(settings.SQLALCHEMY_DATABASE_URI)
    if url.scheme == "sqlite":
        os.remove(url.path[1:])  # remove leading /
    elif url.scheme == "postgresql":
        from app.database import Base, engine

        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def mock_graph():
    with patch("app.services.graph.PreferenceGraph") as mocked:
        g = mocked.return_value.__enter__.return_value
        yield g


@pytest.fixture(scope="function")
def mock_graph_with_exception():
    with patch("app.services.graph.PreferenceGraph") as mocked:
        g = mocked.return_value.__enter__.return_value
        g.setup_user.side_effect = MockNeo4jException
        yield mocked


@pytest.fixture(scope="session")
def mock_gpt():
    with patch("app.services.gpt.generate_gpt_response") as mocked:
        mocked.return_value = "MockGPT"
        yield mocked


@pytest.fixture(scope="function")
def mock_request():
    with patch("requests.request") as mocked:
        yield mocked


@pytest.fixture(scope="function")
def mock_zep_client():
    with patch("app.services.zep.client", autospec=True) as mocked:
        yield mocked


@pytest.fixture(scope="function")
def mock_generate_otp():
    with patch("app.services.otp.generate_otp", autospec=True) as mocked:
        mocked.return_value = "00000"
        yield mocked


@pytest.fixture(scope="function")
def mock_send_otp_email():
    with patch("app.services.aws_email.send_otp_email", autospec=True) as mocked:
        yield mocked


@pytest.fixture(scope="function")
def mock_flowise():
    with patch("app.services.flowise.query", autospec=True) as mocked:
        mocked.return_value = "MockFlowise"
        yield mocked
