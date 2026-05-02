from textblob import TextBlob

from app.models.schemas import SentimentResponse

KEYWORD_BOOST = {
    "helpful": 0.18,
    "supportive": 0.14,
    "clear": 0.08,
    "strict": -0.10,
    "unfair": -0.25,
    "biased": -0.22,
}
BOOST_LIMIT = 0.35


def analyze_sentiment(text: str) -> SentimentResponse:
    polarity = TextBlob(text).sentiment.polarity
    lowered = text.lower()

    keyword_adjustment = 0.0
    for keyword, weight in KEYWORD_BOOST.items():
        if keyword in lowered:
            keyword_adjustment += weight

    if keyword_adjustment > BOOST_LIMIT:
        keyword_adjustment = BOOST_LIMIT
    if keyword_adjustment < -BOOST_LIMIT:
        keyword_adjustment = -BOOST_LIMIT

    score = max(min(round(polarity + keyword_adjustment, 3), 1.0), -1.0)

    if score > 0.2:
        label = "positive"
    elif score < -0.2:
        label = "negative"
    else:
        label = "neutral"

    return SentimentResponse(score=score, label=label)
