def test_connections_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/connections" in paths
