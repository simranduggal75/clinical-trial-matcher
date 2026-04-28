from datetime import date
import re

def parse_age_string(age_str: str) -> int:
    """Convert strings like '18 Years', '6 Months' to integer years."""
    if not age_str:
        return None

    age_str = age_str.strip().lower()

    match = re.search(r"(\d+)", age_str)
    if not match:
        return None

    value = int(match.group(1))

    if "month" in age_str:
        return max(0, value // 12)
    if "week" in age_str:
        return max(0, value // 52)
    return value

def birthdate_to_age(birth_date: str) -> int:
    """Convert birthdate string YYYY-MM-DD to current age."""
    if not birth_date:
        return None
    try:
        bd = date.fromisoformat(birth_date)
        today = date.today()
        return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    except:
        return None