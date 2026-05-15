CONDITION_MAP = {
    "dm":              "diabetes",
    "diabetes mellitus": "diabetes",
    "htn":             "hypertension",
    "high blood pressure": "hypertension",
    "bp":              "hypertension",
    "ca":              "cancer",
    "copd":            "chronic obstructive pulmonary disease",
    "mi":              "myocardial infarction",
    "heart attack":    "myocardial infarction",
    "cad":             "coronary artery disease",
    "ckd":             "chronic kidney disease",
    "afib":            "atrial fibrillation",
    "a-fib":           "atrial fibrillation",
    "ad":              "alzheimer",
    "ra":              "rheumatoid arthritis",
}

def normalize_condition(condition: str) -> str:
    """Normalize common abbreviations to full condition names."""
    return CONDITION_MAP.get(condition.lower().strip(), condition.lower().strip())

def normalize_conditions(conditions: list) -> list:
    """Normalize a list of conditions."""
    return [normalize_condition(c) for c in conditions]

if __name__ == "__main__":
    test = ["DM", "HTN", "CAD", "diabetes mellitus"]
    print(normalize_conditions(test)) 
