from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
response = client.get("/openapi.json")
assert response.status_code == 200, response.text
data = response.json()
assert data["openapi"].startswith("3.")
required = [
    "/auth/register", "/auth/login", "/auth/refresh", "/auth/me",
    "/customers", "/connections", "/meters", "/meter-readings",
    "/tariffs", "/bills/generate", "/payments/{bill_id}",
    "/complaints", "/technicians", "/service-requests",
    "/analytics/connections/{connection_id}/monthly", "/dashboard"
]
missing = [p for p in required if p not in data["paths"]]
assert not missing, f"Missing paths: {missing}"
print("Swagger/OpenAPI verification PASSED")
print("OpenAPI version:", data["openapi"])
print("Number of documented paths:", len(data["paths"]))
