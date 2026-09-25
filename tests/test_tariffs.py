def test_tariffs_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/tariffs" in paths
