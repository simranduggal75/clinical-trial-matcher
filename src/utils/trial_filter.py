from src.utils.age_parser import parse_age_string

def filter_by_age(trials: list, patient_age: int) -> list:
    """Remove trials where patient age is outside min/max range."""
    eligible = []
    for trial in trials:
        min_age = parse_age_string(trial.get("min_age", "0 Years")) or 0
        max_age = parse_age_string(trial.get("max_age", "120 Years")) or 120
        if min_age <= patient_age <= max_age:
            eligible.append(trial)
    return eligible

def filter_by_sex(trials: list, patient_sex: str) -> list:
    """Remove trials that don't accept patient's sex."""
    eligible = []
    for trial in trials:
        trial_sex = trial.get("sex", "ALL").upper()
        if trial_sex == "ALL" or trial_sex == patient_sex.upper():
            eligible.append(trial)
    return eligible

def apply_basic_filters(trials: list, patient: dict) -> list:
    """Apply all basic rule-based filters."""
    age = patient.get("age")
    sex = patient.get("gender", "ALL")

    if age:
        trials = filter_by_age(trials, age)
    if sex:
        trials = filter_by_sex(trials, sex)

    return trials