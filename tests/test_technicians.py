def test_technicians_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/technicians" in paths
