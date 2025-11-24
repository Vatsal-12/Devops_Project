# tests/test_model.py
from app.model import LexiconSentiment

def test_model_with_positive_tokens():
    m = LexiconSentiment()
    res = m.predict(["i", "love", "this", "awesome"])
    assert res["label"] == "POSITIVE"
    assert res["pos_count"] >= 1
    assert 0.0 <= res["score"] <= 1.0

def test_model_with_negative_tokens():
    m = LexiconSentiment()
    res = m.predict(["this", "is", "the", "worst", "experience"])
    assert res["label"] == "NEGATIVE"
    assert res["neg_count"] >= 1

def test_model_with_tie():
    m = LexiconSentiment(positive_lexicon={"good"}, negative_lexicon={"bad"})
    res = m.predict(["good", "bad"])
    assert res["label"] == "NEUTRAL"
    assert res["pos_count"] == 1 and res["neg_count"] == 1

def test_model_no_tokens():
    m = LexiconSentiment()
    res = m.predict([])
    assert res["label"] == "NEUTRAL"
    assert res["score"] == 0.0
