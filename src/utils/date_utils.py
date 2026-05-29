from datetime import datetime, date

def format_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")

def days_since(date_str: str) -> int:
    """Return number of days since a given date string YYYY-MM-DD."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (date.today() - d).days
    except:
        return -1

def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def age_from_birthdate(birth_date: str) -> int:
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = date.today()
        return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    except:
        return -1