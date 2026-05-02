from src.matching.search import TrialSearcher

def test_search_returns_results():
    searcher = TrialSearcher()

    patient = {
        "age":        45,
        "gender":     "female",
        "conditions": ["diabetes", "hypertension"]
    }

    results = searcher.search(patient, top_k=5)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "nct_id" in results[0]
    assert "match_score" in results[0]

def test_search_respects_top_k():
    searcher = TrialSearcher()
    patient  = {"age": 30, "gender": "male", "conditions": ["cancer"]}
    results  = searcher.search(patient, top_k=3)
    assert len(results) <= 3

if __name__ == "__main__":
    test_search_returns_results()
    test_search_respects_top_k()
    print("All tests passed.")