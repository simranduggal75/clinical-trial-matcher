from fastapi.testclient import TestClient
from src.api.main import app

def test_metrics_endpoint():
    with TestClient(app) as c:
        response = c.get("/metrics")
        assert response.status_code == 200
        assert "api_requests_total" in response.text

def test_metrics_after_request():
    with TestClient(app) as c:
        c.get("/health")
        response = c.get("/metrics")
        assert response.status_code == 200
        assert "api_request_latency_seconds" in response.text

def test_match_metrics():
    with TestClient(app) as c:
        payload = {
            "age":        45,
            "gender":     "female",
            "conditions": ["diabetes"],
            "medications": []
        }
        c.post("/match?top_k=3", json=payload)
        response = c.get("/metrics")
        assert "trial_match_score" in response.text

if __name__ == "__main__":
    test_metrics_endpoint()
    test_metrics_after_request()
    test_match_metrics()
    print("All monitoring tests passed.")