def test_meters_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/meters" in paths
