from src.utils.age_parser import birthdate_to_age

def build_patient_profile(raw_patient: dict) -> dict:
    """Convert raw patient dict into a clean profile for matching."""
    age = birthdate_to_age(raw_patient.get("birth_date"))

    conditions = [
        c["display"].lower()
        for c in raw_patient.get("conditions", [])
        if c.get("display")
    ]

    medications = [
        m["display"].lower()
        for m in raw_patient.get("medications", [])
        if m.get("display")
    ]

    return {
        "id":          raw_patient.get("id"),
        "age":         age,
        "gender":      raw_patient.get("gender", "unknown").upper(),
        "conditions":  conditions,
        "medications": medications,
    }

def build_profiles(patients: list) -> list:
    return [build_patient_profile(p) for p in patients]