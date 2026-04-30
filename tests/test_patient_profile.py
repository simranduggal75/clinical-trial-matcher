from src.utils.patient_profile import build_patient_profile

MOCK_PATIENT = {
    "id": "abc123",
    "birth_date": "1990-05-10",
    "gender": "female",
    "conditions": [
        {"code": "44054006", "display": "Diabetes"},
        {"code": "38341003", "display": "Hypertension"}
    ],
    "medications": [
        {"code": "860975", "display": "Metformin"}
    ]
}

def test_profile_fields():
    profile = build_patient_profile(MOCK_PATIENT)
    assert profile["id"] == "abc123"
    assert profile["gender"] == "FEMALE"
    assert isinstance(profile["age"], int)
    assert profile["age"] > 0

def test_conditions_lowercase():
    profile = build_patient_profile(MOCK_PATIENT)
    assert "diabetes" in profile["conditions"]
    assert "hypertension" in profile["conditions"]

def test_medications():
    profile = build_patient_profile(MOCK_PATIENT)
    assert "metformin" in profile["medications"]

if __name__ == "__main__":
    test_profile_fields()
    test_conditions_lowercase()
    test_medications()
    print("All tests passed.")