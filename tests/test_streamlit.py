import requests

API_URL = "http://localhost:8000"

def test_api_health():
    """Check API is running before testing UI flow."""
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"
        print("API health check passed")
    except requests.exceptions.ConnectionError:
        print("API not running — start with: uvicorn src.api.main:app --reload")

def test_match_flow():
    """Simulate what the Streamlit UI sends to the API."""
    payload = {
        "age":        45,
        "gender":     "female",
        "conditions": ["diabetes", "hypertension"],
        "medications": ["metformin"]
    }
    try:
        r = requests.post(f"{API_URL}/match?top_k=5", json=payload, timeout=60)
        assert r.status_code == 200
        data = r.json()
        assert "trials" in data
        assert len(data["trials"]) > 0
        print(f"Match flow passed — {data['total_matches']} trials returned")
        print(f"Top match: {data['trials'][0]['title']}")
    except requests.exceptions.ConnectionError:
        print("API not running — start with: uvicorn src.api.main:app --reload")

if __name__ == "__main__":
    test_api_health()
    test_match_flow()