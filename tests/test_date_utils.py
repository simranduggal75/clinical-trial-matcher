from src.utils.date_utils import is_valid_date, days_since, age_from_birthdate

def test_valid_date():
    assert is_valid_date("2000-01-01") == True
    assert is_valid_date("not-a-date") == False
    assert is_valid_date("2026-13-01") == False

def test_days_since():
    days = days_since("2020-01-01")
    assert days > 0
    assert days_since("invalid") == -1

def test_age_from_birthdate():
    age = age_from_birthdate("2000-01-01")
    assert isinstance(age, int)
    assert age >= 25
    assert age_from_birthdate("invalid") == -1

if __name__ == "__main__":
    test_valid_date()
    test_days_since()
    test_age_from_birthdate()
    print("All tests passed.")