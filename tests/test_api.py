from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app, raise_server_exceptions=True)

def test_health():
    with TestClient(app) as c:
        response = c.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

def test_root():
    with TestClient(app) as c:
        response = c.get("/")
        assert response.status_code == 200

def test_match_endpoint():
    payload = {
        "age":        45,
        "gender":     "female",
        "conditions": ["diabetes", "hypertension"],
        "medications": ["metformin"]
    }
    with TestClient(app) as c:
        response = c.post("/match?top_k=5", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "trials" in data
        assert "total_matches" in data
        assert isinstance(data["trials"], list)

def test_match_invalid_age():
    with TestClient(app) as c:
        payload = {
            "age":        200,
            "gender":     "female",
            "conditions": ["diabetes"]
        }
        response = c.post("/match", json=payload)
        assert response.status_code == 422

if __name__ == "__main__":
    test_health()
    test_root()
    test_match_endpoint()
    test_match_invalid_age()
    print("All API tests passed.")