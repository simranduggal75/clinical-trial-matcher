from src.utils.age_parser import parse_age_string, birthdate_to_age

def test_parse_age_string():
    assert parse_age_string("18 Years") == 18
    assert parse_age_string("6 Months") == 0
    assert parse_age_string("N/A") == None
    assert parse_age_string("") == None

def test_birthdate_to_age():
    age = birthdate_to_age("2000-01-01")
    assert isinstance(age, int)
    assert age >= 25

if __name__ == "__main__":
    test_parse_age_string()
    test_birthdate_to_age()
    print("All tests passed.")