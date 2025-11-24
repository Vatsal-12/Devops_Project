# app/preprocess.py
import re
from typing import List

def clean_text(text: str) -> str:
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = re.sub(r"(?!\B'\b)[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> List[str]:
    cleaned = clean_text(text)
    if cleaned == "":
        return []
    return cleaned.split()
