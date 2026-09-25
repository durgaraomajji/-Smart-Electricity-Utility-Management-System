def test_analytics_path_documented(client):
    paths=client.get("/openapi.json").json()["paths"]
    assert "/analytics/connections/{connection_id}/monthly" in paths
