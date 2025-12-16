from fastapi import APIRouter
from api.models import HealthResponse
from datetime import datetime

health_router = APIRouter()

@health_router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )