from fastapi import APIRouter

from app.models.schemas import SentimentRequest, SentimentResponse
from app.services.sentiment_service import analyze_sentiment

router = APIRouter(tags=["sentiment"])


@router.post("/sentiment/analyze", response_model=SentimentResponse)
async def analyze_sentiment_route(payload: SentimentRequest) -> SentimentResponse:
    return analyze_sentiment(payload.text)
