# from fixtures import api_request_context
from .config import SERVER_URL


def test_get_server_status(api_request_context):
    response = api_request_context.get(f"{SERVER_URL}/")
    assert response.ok
    data = response.json()
    assert "Status" in data
    assert data["Status"] == "OK"


# pytest tests/e2e -v -s
