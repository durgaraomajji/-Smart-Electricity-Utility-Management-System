def test_openapi(client):
    response=client.get("/openapi.json")
    assert response.status_code==200
    assert "/auth/login" in response.json()["paths"]
