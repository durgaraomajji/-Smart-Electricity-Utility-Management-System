def test_complaints_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/complaints" in paths
