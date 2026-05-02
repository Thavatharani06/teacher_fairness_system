from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

FairnessLabel = Literal["undervalued", "fair", "overvalued"]
SentimentLabel = Literal["negative", "neutral", "positive"]


class StudentBase(BaseModel):
    student_id: str = Field(min_length=3, max_length=30)
    student_name: str = Field(min_length=2, max_length=80)
    teacher: str = Field(min_length=2, max_length=80)
    attendance: float = Field(ge=0, le=100)
    cgpa: float = Field(ge=0, le=10)
    past_marks: float = Field(ge=0, le=100)


class FairnessRequest(StudentBase):
    teacher_score: float = Field(ge=0, le=100)
    feedback_text: str = Field(default="", max_length=1000)


class FairnessResult(BaseModel):
    expected_score: float
    teacher_score: float
    fairness_score: float
    fairness_result: FairnessLabel
    delta: float
    is_anomaly: bool


class EvaluationRecord(FairnessRequest):
    sentiment_score: float
    sentiment_label: SentimentLabel
    fairness: FairnessResult
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SentimentRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1500)


class SentimentResponse(BaseModel):
    score: float
    label: SentimentLabel


class TeacherFairnessStat(BaseModel):
    teacher: str
    total_evaluations: int
    undervalued_count: int
    undervalued_ratio: float
    average_fairness_score: float
    is_bias_flagged: bool


class DashboardStats(BaseModel):
    total_evaluations: int
    fair_count: int
    undervalued_count: int
    overvalued_count: int
    anomalies_count: int
    teacher_stats: list[TeacherFairnessStat]


class EvaluationFilterParams(BaseModel):
    search: str | None = None
    teacher: str | None = None
    fairness_result: FairnessLabel | None = None
    sentiment_label: SentimentLabel | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=500)

    @field_validator("search", "teacher")
    @classmethod
    def strip_or_none(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        return cleaned or None
