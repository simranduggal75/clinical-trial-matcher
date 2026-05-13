def validate_patient(patient: dict) -> list:
    """Returns list of errors. Empty list means valid."""
    errors = []

    age = patient.get("age")
    if age is None:
        errors.append("age is required")
    elif not isinstance(age, int) or age < 0 or age > 120:
        errors.append("age must be between 0 and 120")

    gender = patient.get("gender", "")
    if gender.lower() not in ["male", "female"]:
        errors.append("gender must be male or female")

    conditions = patient.get("conditions", [])
    if not conditions:
        errors.append("at least one condition is required")

    return errors