import csv
import io
import re

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.models.schemas import (
    EvaluationFilterParams,
    EvaluationRecord,
    FairnessRequest,
    SentimentResponse,
    TeacherFairnessStat,
)
from app.services.fairness_service import calculate_fairness, calculate_teacher_bias_stats
from app.services.sentiment_service import analyze_sentiment
from app.utils.db import get_db

router = APIRouter(tags=["fairness"])


@router.post("/evaluations/calculate-fairness", response_model=EvaluationRecord)
async def calculate_fairness_route(payload: FairnessRequest) -> EvaluationRecord:
    db = get_db()
    evaluations = db["evaluations"]
    historical = await evaluations.find({}, {"delta": 1, "_id": 0}).to_list(length=2000)
    deltas = [item.get("delta", 0.0) for item in historical]
    fairness = calculate_fairness(payload, deltas)
    sentiment: SentimentResponse = analyze_sentiment(payload.feedback_text or "")

    record = EvaluationRecord(
        **payload.model_dump(),
        sentiment_score=sentiment.score,
        sentiment_label=sentiment.label,
        fairness=fairness,
    )
    document = {
        **payload.model_dump(),
        "expected_score": fairness.expected_score,
        "fairness_score": fairness.fairness_score,
        "fairness_result": fairness.fairness_result,
        "delta": fairness.delta,
        "is_anomaly": fairness.is_anomaly,
        "sentiment_score": sentiment.score,
        "sentiment_label": sentiment.label,
        "created_at": record.created_at,
    }
    await evaluations.insert_one(document)
    return record


@router.post("/evaluations/batch-calculate", response_model=list[EvaluationRecord])
async def batch_calculate_fairness(payload: list[FairnessRequest]) -> list[EvaluationRecord]:
    results: list[EvaluationRecord] = []
    for item in payload:
        results.append(await calculate_fairness_route(item))
    return results


@router.get("/teachers/fairness-score", response_model=list[TeacherFairnessStat])
async def teacher_fairness_scores() -> list[TeacherFairnessStat]:
    db = get_db()
    rows = await db["evaluations"].aggregate(
        [
            {
                "$group": {
                    "_id": "$teacher",
                    "docs": {
                        "$push": {
                            "fairness_result": "$fairness_result",
                            "fairness_score": "$fairness_score",
                        }
                    },
                }
            }
        ]
    ).to_list(length=None)
    return [calculate_teacher_bias_stats(row["_id"], row["docs"]) for row in rows]


def build_filter_query(params: EvaluationFilterParams) -> dict:
    query: dict = {}
    if params.teacher:
        query["teacher"] = params.teacher
    if params.fairness_result:
        query["fairness_result"] = params.fairness_result
    if params.sentiment_label:
        query["sentiment_label"] = params.sentiment_label
    if params.search:
        safe = re.escape(params.search)
        query["$or"] = [
            {"student_name": {"$regex": safe, "$options": "i"}},
            {"student_id": {"$regex": safe, "$options": "i"}},
            {"teacher": {"$regex": safe, "$options": "i"}},
        ]
    return query


@router.get("/evaluations")
async def list_evaluations(
    search: str | None = Query(default=None),
    teacher: str | None = Query(default=None),
    fairness_result: str | None = Query(default=None),
    sentiment_label: str | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
):
    params = EvaluationFilterParams(
        search=search,
        teacher=teacher,
        fairness_result=fairness_result,
        sentiment_label=sentiment_label,
        skip=skip,
        limit=limit,
    )
    db = get_db()
    query = build_filter_query(params)
    rows = await db["evaluations"].find(query).skip(params.skip).limit(params.limit).to_list(length=params.limit)
    for row in rows:
        row["_id"] = str(row["_id"])
    return rows


@router.get("/evaluations/export.csv")
async def export_evaluations_csv(
    search: str | None = Query(default=None),
    teacher: str | None = Query(default=None),
    fairness_result: str | None = Query(default=None),
    sentiment_label: str | None = Query(default=None),
):
    params = EvaluationFilterParams(
        search=search,
        teacher=teacher,
        fairness_result=fairness_result,
        sentiment_label=sentiment_label,
    )
    db = get_db()
    query = build_filter_query(params)
    rows = await db["evaluations"].find(query).to_list(length=5000)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "student_id",
            "student_name",
            "teacher",
            "teacher_score",
            "expected_score",
            "fairness_score",
            "fairness_result",
            "delta",
            "is_anomaly",
            "sentiment_score",
            "sentiment_label",
        ]
    )
    for row in rows:
        writer.writerow(
            [
                row.get("student_id"),
                row.get("student_name"),
                row.get("teacher"),
                row.get("teacher_score"),
                row.get("expected_score"),
                row.get("fairness_score"),
                row.get("fairness_result"),
                row.get("delta"),
                row.get("is_anomaly"),
                row.get("sentiment_score"),
                row.get("sentiment_label"),
            ]
        )

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=evaluations.csv"},
    )
