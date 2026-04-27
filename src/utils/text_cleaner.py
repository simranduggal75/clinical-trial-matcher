import re

def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def remove_special_chars(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s.,;:()\-]", "", text)

def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())

def truncate(text: str, max_len: int = 512) -> str:
    return text[:max_len] if len(text) > max_len else text