from src.utils.condition_normalizer import normalize_condition, normalize_conditions

def test_normalize_abbreviation():
    assert normalize_condition("DM") == "diabetes"
    assert normalize_condition("HTN") == "hypertension"
    assert normalize_condition("MI") == "myocardial infarction"

def test_normalize_unknown():
    assert normalize_condition("lupus") == "lupus"

def test_normalize_list():
    result = normalize_conditions(["DM", "HTN", "cancer"])
    assert result == ["diabetes", "hypertension", "cancer"]

def test_case_insensitive():
    assert normalize_condition("htn") == normalize_condition("HTN")

if __name__ == "__main__":
    test_normalize_abbreviation()
    test_normalize_unknown()
    test_normalize_list()
    test_case_insensitive()
    print("All tests passed.") 
