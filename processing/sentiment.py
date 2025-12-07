# processing/sentiment.py
from transformers import pipeline
from functools import lru_cache

NEG_WORDS = ["poor", "bad", "problem", "issue", "issues", "expensive", "noisy", "noise", "slow", "worst"]
POS_WORDS = ["great", "best", "amazing", "silent", "quiet", "efficient", "saving", "saves", "energy saving"]


@lru_cache(maxsize=1)
def get_model():
    return pipeline("sentiment-analysis")


def sentiment_score(text: str) -> float:
    if not text:
        return 0.0

    model = get_model()
    res = model(text[:512])[0]

    score = res["score"]
    label = res["label"].lower()
    if "neg" in label:
        score = -score

    low = text.lower()

    # Lexical nudges (help with short snippets)
    for w in NEG_WORDS:
        if w in low:
            score -= 0.15

    for w in POS_WORDS:
        if w in low:
            score += 0.15

    # clamp
    score = max(min(score, 1.0), -1.0)
    return score
