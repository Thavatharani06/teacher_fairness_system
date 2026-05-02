from datetime import datetime

from pydantic import BaseModel, Field

from app.models.schemas import FairnessLabel, SentimentLabel


class EvaluationModel(BaseModel):
    student_id: str
    student_name: str
    teacher: str
    teacher_score: float = Field(ge=0, le=100)
    expected_score: float
    fairness_score: float
    fairness_result: FairnessLabel
    delta: float
    is_anomaly: bool
    sentiment_score: float
    sentiment_label: SentimentLabel
    feedback_text: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
