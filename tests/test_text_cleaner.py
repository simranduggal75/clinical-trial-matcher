from src.utils.text_cleaner import clean_text, truncate, normalize_whitespace

def test_clean_text():
    assert clean_text("  hello   world  ") == "hello world"
    assert clean_text("line1\r\nline2") == "line1 line2"

def test_truncate():
    assert truncate("hello world", max_len=5) == "hello"
    assert truncate("hi", max_len=10) == "hi"

def test_normalize_whitespace():
    assert normalize_whitespace("too   many    spaces") == "too many spaces"

if __name__ == "__main__":
    test_clean_text()
    test_truncate()
    test_normalize_whitespace()
    print("All tests passed.")