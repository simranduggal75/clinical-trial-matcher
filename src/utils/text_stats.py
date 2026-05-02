def word_count(text: str) -> int:
    return len(text.split())

def char_count(text: str) -> int:
    return len(text)

def avg_word_length(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return round(sum(len(w) for w in words) / len(words), 2)

def sentence_count(text: str) -> int:
    return len([s for s in text.split(".") if s.strip()]) 
