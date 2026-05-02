from fastapi import APIRouter

from app.models.schemas import DashboardStats
from app.services.dashboard_service import fetch_dashboard_stats

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/stats", response_model=DashboardStats)
async def dashboard_stats() -> DashboardStats:
    return DashboardStats(**await fetch_dashboard_stats())
