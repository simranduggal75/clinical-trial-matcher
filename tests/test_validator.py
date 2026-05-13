from src.utils.validator import validate_patient

def test_valid_patient():
    p = {"age": 45, "gender": "female", "conditions": ["diabetes"]}
    assert validate_patient(p) == []

def test_invalid_age():
    p = {"age": 200, "gender": "female", "conditions": ["diabetes"]}
    assert any("age" in e for e in validate_patient(p))

def test_missing_conditions():
    p = {"age": 30, "gender": "male", "conditions": []}
    assert any("condition" in e for e in validate_patient(p))

def test_invalid_gender():
    p = {"age": 30, "gender": "unknown", "conditions": ["cancer"]}
    assert any("gender" in e for e in validate_patient(p))

if __name__ == "__main__":
    test_valid_patient()
    test_invalid_age()
    test_missing_conditions()
    test_invalid_gender()
    print("All tests passed.")