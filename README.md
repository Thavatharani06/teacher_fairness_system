# AI-Based Teacher Fairness & Academic Evaluation System

Production-ready demo stack:
- Frontend: React + Axios + Chart.js
- Backend: FastAPI
- Database: MongoDB (Motor async driver)

## Folder Structure

```text
teacher_fairness_system/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── scripts/seed_data.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Backend Setup (FastAPI)

1. Open terminal at `teacher_fairness_system/backend`
2. Create virtual env and install:
   - `python -m venv .venv`
   - Windows: `.venv\\Scripts\\activate`
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Run API:
   - `uvicorn app.main:app --reload`

Backend base URL: `http://localhost:8000`

## Frontend Setup (React)

1. Open terminal at `teacher_fairness_system/frontend`
2. Install packages:
   - `npm install`
3. (Optional) create `.env`:
   - `VITE_API_BASE_URL=http://localhost:8000/api/v1`
4. Run app:
   - `npm run dev`

Frontend URL: `http://localhost:5173`

## MongoDB Setup (Atlas)

1. Create a MongoDB Atlas cluster.
2. Add your current IP in Atlas Network Access.
3. Create a database user.
4. In `backend`, create `.env` with:
   - `MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=<appName>`
   - `MONGODB_DB_NAME=teacher_fairness`

## Seed 500 Sample Records

From `teacher_fairness_system/backend`:
- `python -m scripts.seed_data`

This script inserts 500 realistic student evaluation records with variation in:
- attendance, CGPA, past marks
- fairness outcomes (fair/under/over)
- sentiment labels with keyword boost effects

## API Endpoints

- `POST /api/v1/evaluations/calculate-fairness`
- `POST /api/v1/evaluations/batch-calculate`
- `GET /api/v1/teachers/fairness-score`
- `POST /api/v1/sentiment/analyze`
- `GET /api/v1/dashboard/stats`
- `GET /api/v1/evaluations`
- `GET /api/v1/evaluations/export.csv`

## Example Request (Fairness)

`POST /api/v1/evaluations/calculate-fairness`

```json
{
  "student_id": "STU0101",
  "student_name": "Asha",
  "teacher": "Dr. Meena",
  "attendance": 90,
  "cgpa": 8.7,
  "past_marks": 84,
  "teacher_score": 72,
  "feedback_text": "The teacher is strict but helpful."
}
```

## Fairness Logic (Explainable)

- Inputs: attendance, CGPA, past marks
- Normalization: min-max normalization per feature
- Weighted expected score:
  - attendance: 30%
  - CGPA: 35%
  - past marks: 35%
- Delta = `teacher_score - expected_score`
- Labels:
  - `< -10`: undervalued
  - `-10 to 10`: fair
  - `> 10`: overvalued
- Anomaly: z-score on delta (`|z| >= 2.0`)
- Teacher bias flag: undervalued ratio `> 30%`

## Sentiment Logic (Explainable)

- Base score from TextBlob polarity
- Keyword adjustment (boost/dampen), capped to avoid extreme shifts
- Output:
  - `score` in `[-1, 1]`
  - `label` in `positive | neutral | negative`

