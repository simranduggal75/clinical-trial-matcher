def score_trial(trial: dict, patient: dict) -> float:
    """
    Boost FAISS similarity score based on rule-based signals.
    Returns adjusted score between 0 and 1.
    """
    score = trial.get("match_score", 0.0)

    patient_conditions = [c.lower() for c in patient.get("conditions", [])]
    trial_conditions   = [c.lower() for c in trial.get("conditions", [])]

    # boost if condition overlap
    overlap = set(patient_conditions) & set(trial_conditions)
    if overlap:
        score += 0.05 * len(overlap)

    # boost if gender matches exactly
    trial_sex  = trial.get("sex", "ALL").upper()
    patient_sex = patient.get("gender", "").upper()
    if trial_sex == patient_sex:
        score += 0.02

    # cap at 1.0
    return round(min(score, 1.0), 4)

def rerank_trials(trials: list, patient: dict) -> list:
    """Re-rank trials by adjusted score."""
    for trial in trials:
        trial["adjusted_score"] = score_trial(trial, patient)
    return sorted(trials, key=lambda x: x["adjusted_score"], reverse=True) 
