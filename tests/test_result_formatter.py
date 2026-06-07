from src.utils.result_formatter import format_trial_result, format_results, results_to_text

MOCK_TRIAL = {
    "nct_id":      "NCT001",
    "title":       "Diabetes Study",
    "conditions":  ["diabetes", "hypertension"],
    "match_score": 0.8929,
    "min_age":     "18 Years",
    "max_age":     "75 Years",
    "sex":         "ALL"
}

def test_format_single():
    result = format_trial_result(MOCK_TRIAL)
    assert result["nct_id"] == "NCT001"
    assert result["match_score"] == 0.8929
    assert "clinicaltrials.gov" in result["url"]
    assert result["age_range"] == "18 Years - 75 Years"

def test_format_results():
    results = format_results([MOCK_TRIAL])
    assert len(results) == 1
    assert results[0]["conditions"] == "diabetes, hypertension"

def test_results_to_text():
    text = results_to_text([MOCK_TRIAL])
    assert "NCT001" in text
    assert "Diabetes Study" in text

def test_empty_results():
    assert results_to_text([]) == "No matching trials found."

if __name__ == "__main__":
    test_format_single()
    test_format_results()
    test_results_to_text()
    test_empty_results()
    print("All tests passed.") 
