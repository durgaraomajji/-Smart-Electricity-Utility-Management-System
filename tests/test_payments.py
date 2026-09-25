def test_payments_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/payments/{bill_id}" in paths
