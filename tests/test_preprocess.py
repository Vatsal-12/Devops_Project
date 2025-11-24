# tests/test_preprocess.py
from app.preprocess import clean_text, tokenize

def test_clean_text_basic():
    assert clean_text("Hello WORLD!!") == "hello world"

def test_clean_text_urls_and_mentions():
    assert clean_text("Check http://example.com @user") == "check"

def test_tokenize_empty_and_none():
    assert tokenize("") == []
    assert tokenize(None) == []

def test_tokenize_basic():
    assert tokenize("I love Python!") == ["i", "love", "python"]
