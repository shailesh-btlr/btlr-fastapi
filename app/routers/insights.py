from app.database import get_db
from fastapi import APIRouter, Depends
from app.schemas.insights import Insight, DebugInsight
from app.services import insights
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()


@router.get("", response_model=DebugInsight)
def generate_insight(
    user_id: int,
    touchpoint_id: int,
    role_id: int,
    max_tokens: Optional[int] = 8000,
    db: Session = Depends(get_db)
):
    return insights.generate_insight(
        db,
        user_id,
        touchpoint_id,
        role_id,
        max_tokens
    )


@router.get("/flowise", response_model=DebugInsight)
def generate_insight_with_flowise(
    user_id: int,
    touchpoint_id: int,
    role_id: int,
    max_tokens: Optional[int] = 8000,
    db: Session = Depends(get_db)
):
    return insights.generate_insight(
        db,
        user_id,
        touchpoint_id,
        role_id,
        max_tokens
    )
