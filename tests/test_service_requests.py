def test_service_requests_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/service-requests" in paths
