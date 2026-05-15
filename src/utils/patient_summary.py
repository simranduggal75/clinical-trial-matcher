from src.utils.age_parser import birthdate_to_age

def summarize_patient(patient: dict) -> str:
    """Generate a human-readable summary of a patient profile."""
    age      = patient.get("age") or birthdate_to_age(patient.get("birth_date"))
    gender   = patient.get("gender", "unknown")
    conditions  = patient.get("conditions", [])
    medications = patient.get("medications", [])

    summary = f"Patient: {gender}, age {age}.\n"

    if conditions:
        summary += f"Conditions: {', '.join(conditions)}.\n"
    else:
        summary += "Conditions: none recorded.\n"

    if medications:
        summary += f"Medications: {', '.join(medications)}.\n"
    else:
        summary += "Medications: none recorded.\n"

    return summary.strip()

if __name__ == "__main__":
    p = {
        "age": 45,
        "gender": "female",
        "conditions": ["diabetes", "hypertension"],
        "medications": ["metformin"]
    }
    print(summarize_patient(p)) 
