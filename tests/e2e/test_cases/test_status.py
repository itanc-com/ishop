from tests.e2e.config import SERVER_URL


def test_get_server_status(api_request_context):
    response = api_request_context.get(f"{SERVER_URL}/")
    assert response.ok
    data = response.json()
    assert "status" in data
    assert data["status"] == "OK"
