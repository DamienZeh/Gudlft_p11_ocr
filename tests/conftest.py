import server
import pytest


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    clients = server.app.test_client()
    return clients
