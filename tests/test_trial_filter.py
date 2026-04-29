from src.utils.trial_filter import filter_by_age, filter_by_sex, apply_basic_filters

MOCK_TRIALS = [
    {"nct_id": "NCT001", "min_age": "18 Years", "max_age": "65 Years", "sex": "ALL"},
    {"nct_id": "NCT002", "min_age": "0 Years",  "max_age": "12 Years", "sex": "ALL"},
    {"nct_id": "NCT003", "min_age": "18 Years", "max_age": "80 Years", "sex": "FEMALE"},
    {"nct_id": "NCT004", "min_age": "30 Years", "max_age": "120 Years","sex": "MALE"},
]

def test_filter_by_age():
    result = filter_by_age(MOCK_TRIALS, patient_age=25)
    ids = [t["nct_id"] for t in result]
    assert "NCT001" in ids
    assert "NCT002" not in ids

def test_filter_by_sex():
    result = filter_by_sex(MOCK_TRIALS, patient_sex="FEMALE")
    ids = [t["nct_id"] for t in result]
    assert "NCT003" in ids
    assert "NCT004" not in ids

def test_apply_basic_filters():
    patient = {"age": 35, "gender": "female"}
    result = apply_basic_filters(MOCK_TRIALS, patient)
    ids = [t["nct_id"] for t in result]
    assert "NCT001" in ids
    assert "NCT002" not in ids
    assert "NCT004" not in ids

if __name__ == "__main__":
    test_filter_by_age()
    test_filter_by_sex()
    test_apply_basic_filters()
    print("All tests passed.")