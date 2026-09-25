def test_readings_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/meter-readings" in paths
