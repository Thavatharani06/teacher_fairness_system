from app.services.fairness_service import calculate_teacher_bias_stats
from app.utils.db import get_db


async def fetch_dashboard_stats() -> dict:
    db = get_db()
    evaluations = db["evaluations"]
    total_evaluations = await evaluations.count_documents({})
    fair_count = await evaluations.count_documents({"fairness_result": "fair"})
    undervalued_count = await evaluations.count_documents({"fairness_result": "undervalued"})
    overvalued_count = await evaluations.count_documents({"fairness_result": "overvalued"})
    anomalies_count = await evaluations.count_documents({"is_anomaly": True})

    teacher_pipeline = [
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
    teacher_groups = await evaluations.aggregate(teacher_pipeline).to_list(length=None)
    teacher_stats = [
        calculate_teacher_bias_stats(item["_id"], item["docs"]).model_dump()
        for item in teacher_groups
    ]

    return {
        "total_evaluations": total_evaluations,
        "fair_count": fair_count,
        "undervalued_count": undervalued_count,
        "overvalued_count": overvalued_count,
        "anomalies_count": anomalies_count,
        "teacher_stats": teacher_stats,
    }
