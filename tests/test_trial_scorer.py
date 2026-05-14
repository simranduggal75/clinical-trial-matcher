from src.utils.trial_scorer import score_trial, rerank_trials

MOCK_PATIENT = {
    "age":        45,
    "gender":     "female",
    "conditions": ["diabetes", "hypertension"]
}

MOCK_TRIALS = [
    {"nct_id": "NCT001", "title": "Diabetes Study",    "conditions": ["diabetes"],              "sex": "ALL",    "match_score": 0.80},
    {"nct_id": "NCT002", "title": "Cancer Study",      "conditions": ["cancer"],                "sex": "ALL",    "match_score": 0.75},
    {"nct_id": "NCT003", "title": "Hypertension Study","conditions": ["hypertension"],          "sex": "FEMALE", "match_score": 0.70},
]

def test_score_boost_on_condition_overlap():
    score = score_trial(MOCK_TRIALS[0], MOCK_PATIENT)
    assert score > MOCK_TRIALS[0]["match_score"]

def test_score_boost_on_gender_match():
    score = score_trial(MOCK_TRIALS[2], MOCK_PATIENT)
    assert score > MOCK_TRIALS[2]["match_score"]

def test_score_capped_at_one():
    trial = {"conditions": ["diabetes"], "sex": "FEMALE", "match_score": 0.99}
    score = score_trial(trial, MOCK_PATIENT)
    assert score <= 1.0

def test_rerank_order():
    ranked = rerank_trials(MOCK_TRIALS.copy(), MOCK_PATIENT)
    scores = [t["adjusted_score"] for t in ranked]
    assert scores == sorted(scores, reverse=True)

if __name__ == "__main__":
    test_score_boost_on_condition_overlap()
    test_score_boost_on_gender_match()
    test_score_capped_at_one()
    test_rerank_order()
    print("All tests passed.") 
