# app/model.py
from collections import Counter

POSITIVE = {
    "good", "great", "excellent", "awesome", "amazing", "love", "liked", "happy",
    "fantastic", "nice", "wonderful", "best", "positive", "enjoy", "enjoyed"
}
NEGATIVE = {
    "bad", "terrible", "awful", "hate", "hated", "worst", "sad", "angry",
    "disappoint", "disappointed", "poor", "negative", "problem", "issue"
}

class LexiconSentiment:
    def __init__(self, positive_lexicon=None, negative_lexicon=None):
        self.pos = set(positive_lexicon or POSITIVE)
        self.neg = set(negative_lexicon or NEGATIVE)

    def predict(self, tokens):
        if not tokens:
            return {"label": "NEUTRAL", "score": 0.0, "pos_count": 0, "neg_count": 0, "tokens_total": 0}

        counts = Counter()
        for t in tokens:
            if t in self.pos:
                counts["pos"] += 1
            elif t in self.neg:
                counts["neg"] += 1
            else:
                counts["other"] += 1

        pos = counts.get("pos", 0)
        neg = counts.get("neg", 0)
        total = pos + neg

        if total == 0:
            label = "NEUTRAL"
            score = 0.0
        else:
            if pos > neg:
                label = "POSITIVE"
                score = pos / total
            elif neg > pos:
                label = "NEGATIVE"
                score = neg / total
            else:
                label = "NEUTRAL"
                score = 0.5

        opinion_density = total / len(tokens) if len(tokens) > 0 else 0
        final_score = score * opinion_density

        return {
            "label": label,
            "score": round(final_score, 3),
            "pos_count": pos,
            "neg_count": neg,
            "tokens_total": len(tokens)
        }
