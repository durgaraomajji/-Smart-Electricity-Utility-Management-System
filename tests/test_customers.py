def test_customer_path_documented(client):
    assert client.get("/openapi.json").status_code==200
    assert "/customers" in client.get("/openapi.json").json()["paths"]
