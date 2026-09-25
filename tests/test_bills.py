def test_bills_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/bills/generate" in paths
