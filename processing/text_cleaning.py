# processing/text_cleaning.py
import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", " ", text)          # URLs
    text = re.sub(r"[^a-z0-9\s]", " ", text)      # keep alphanum
    text = re.sub(r"\b\d+\b", " ", text)          # drop isolated numbers
    text = re.sub(r"\s+", " ", text).strip()
    return text
