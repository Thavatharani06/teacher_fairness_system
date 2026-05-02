from app.models.schemas import FairnessRequest, FairnessResult, TeacherFairnessStat
from app.utils.stats import min_max_normalize, safe_z_score

ATTENDANCE_WEIGHT = 0.30
CGPA_WEIGHT = 0.35
PAST_MARKS_WEIGHT = 0.35
ANOMALY_ZSCORE_THRESHOLD = 2.0
BIAS_UNDERVALUE_THRESHOLD = 0.30


def calculate_expected_score(request: FairnessRequest) -> float:
    attendance_norm = min_max_normalize(request.attendance, 0, 100)
    cgpa_norm = min_max_normalize(request.cgpa, 0, 10)
    past_marks_norm = min_max_normalize(request.past_marks, 0, 100)

    expected = (
        attendance_norm * ATTENDANCE_WEIGHT
        + cgpa_norm * CGPA_WEIGHT
        + past_marks_norm * PAST_MARKS_WEIGHT
    ) * 100
    return round(expected, 2)


def fairness_label_from_delta(delta: float) -> str:
    if delta < -10:
        return "undervalued"
    if delta > 10:
        return "overvalued"
    return "fair"


def calculate_fairness(request: FairnessRequest, historical_deltas: list[float]) -> FairnessResult:
    expected_score = calculate_expected_score(request)
    delta = round(request.teacher_score - expected_score, 2)
    z_score = abs(safe_z_score(delta, historical_deltas + [delta]))
    is_anomaly = z_score >= ANOMALY_ZSCORE_THRESHOLD
    fairness_score = round(100 - abs(delta), 2)

    return FairnessResult(
        expected_score=expected_score,
        teacher_score=request.teacher_score,
        fairness_score=max(fairness_score, 0),
        fairness_result=fairness_label_from_delta(delta),
        delta=delta,
        is_anomaly=is_anomaly,
    )


def calculate_teacher_bias_stats(teacher: str, docs: list[dict]) -> TeacherFairnessStat:
    total = len(docs)
    undervalued = sum(1 for item in docs if item.get("fairness_result") == "undervalued")
    avg_score = round(sum(item.get("fairness_score", 0) for item in docs) / max(total, 1), 2)
    ratio = round(undervalued / max(total, 1), 3)
    return TeacherFairnessStat(
        teacher=teacher,
        total_evaluations=total,
        undervalued_count=undervalued,
        undervalued_ratio=ratio,
        average_fairness_score=avg_score,
        is_bias_flagged=ratio > BIAS_UNDERVALUE_THRESHOLD,
    )
