
def is_valid_age(age) -> bool:
    return isinstance(age, int) and 0 <= age <= 120

def is_valid_gender(gender: str) -> bool:
    return gender.upper() in ["MALE", "FEMALE", "ALL"]

def is_valid_nct_id(nct_id: str) -> bool:
    return isinstance(nct_id, str) and nct_id.startswith("NCT")