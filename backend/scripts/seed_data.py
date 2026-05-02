import asyncio
import os
import random
from datetime import datetime, timedelta

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.models.schemas import FairnessRequest
from app.services.fairness_service import calculate_fairness
from app.services.sentiment_service import analyze_sentiment

load_dotenv()
MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGODB_DB_NAME", "teacher_fairness")
TOTAL_RECORDS = 500

TEACHERS = [
    "Dr. Meena",
    "Prof. Arjun",
    "Dr. Priya",
    "Prof. Karthik",
    "Dr. Lakshmi",
]

SENTIMENTS = [
    "The teacher is very helpful and clear in explanations.",
    "The class is strict but supportive in assignments.",
    "Evaluation felt unfair and biased in viva.",
    "Helpful sessions but strict marking in tests.",
    "Great mentoring and supportive feedback.",
]


def build_student(idx: int) -> dict:
    attendance = round(random.uniform(55, 99), 2)
    cgpa = round(random.uniform(5.5, 9.9), 2)
    past_marks = round(random.uniform(45, 98), 2)
    teacher = random.choice(TEACHERS)
    feedback = random.choice(SENTIMENTS)

    expected_proxy = (attendance * 0.3 + (cgpa * 10) * 0.35 + past_marks * 0.35) / 1.0
    teacher_score = round(max(min(expected_proxy + random.uniform(-20, 20), 100), 0), 2)

    return {
        "student_id": f"STU{idx:04d}",
        "student_name": f"Student {idx}",
        "teacher": teacher,
        "attendance": attendance,
        "cgpa": cgpa,
        "past_marks": past_marks,
        "teacher_score": teacher_score,
        "feedback_text": feedback,
    }


async def main() -> None:
    random.seed(42)
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    evaluations = db["evaluations"]
    await evaluations.delete_many({})

    historical_deltas: list[float] = []
    docs = []
    now = datetime.utcnow()

    for idx in range(1, TOTAL_RECORDS + 1):
        base = build_student(idx)
        fairness = calculate_fairness(FairnessRequest(**base), historical_deltas)
        sentiment = analyze_sentiment(base["feedback_text"])
        historical_deltas.append(fairness.delta)
        docs.append(
            {
                **base,
                "expected_score": fairness.expected_score,
                "fairness_score": fairness.fairness_score,
                "fairness_result": fairness.fairness_result,
                "delta": fairness.delta,
                "is_anomaly": fairness.is_anomaly,
                "sentiment_score": sentiment.score,
                "sentiment_label": sentiment.label,
                "created_at": now - timedelta(days=random.randint(0, 120)),
            }
        )

    await evaluations.insert_many(docs)
    await evaluations.create_index("teacher")
    await evaluations.create_index("fairness_result")
    await evaluations.create_index([("teacher", 1), ("fairness_result", 1)])
    print(f"Seeded {TOTAL_RECORDS} records into {DB_NAME}.evaluations")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
