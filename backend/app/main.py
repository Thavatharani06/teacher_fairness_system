from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.dashboard_routes import router as dashboard_router
from app.routes.fairness_routes import router as fairness_router
from app.routes.sentiment_routes import router as sentiment_router
from app.utils.db import connect_to_db
from app.utils.errors import register_exception_handlers


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Teacher Fairness & Academic Evaluation API",
        version="1.0.0",
        description="Production-ready demo API for fairness and sentiment evaluation.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(fairness_router, prefix="/api/v1")
    app.include_router(sentiment_router, prefix="/api/v1")
    app.include_router(dashboard_router, prefix="/api/v1")
    register_exception_handlers(app)
    return app


app = create_app()
