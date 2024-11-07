from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_experiences import (
    CheckIn,
    AssignmentAcceptance,
    ExperienceAssignment,
    UserExperience,
)
from app.services import user_experiences

router = APIRouter()


@router.post("/check-in", response_model=UserExperience)
async def check_in(request: CheckIn, db: Session = Depends(get_db)):
    return user_experiences.check_in(
        db, user_id=request.user_id, business_id=request.business_id
    )


@router.get("/{id}", response_model=UserExperience)
async def get_experience(id: int, db: Session = Depends(get_db)):
    return user_experiences.get_experience(db, id)


@router.get("/{id}/diagram.svg")
async def get_diagram(id: int, db: Session = Depends(get_db)):
    return Response(
        content=user_experiences.get_diagram(db, id),
        media_type="image/svg+xml",
    )


@router.get("", response_model=list[UserExperience])
async def get_experiences(
    user_id: Optional[int] = None,
    business_id: Optional[int] = None,
    state: List[str] = Query(None),
    created_from: Optional[datetime] = None,
    created_to: Optional[datetime] = None,
    updated_from: Optional[datetime] = None,
    updated_to: Optional[datetime] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(100, gt=0, le=1000),
    db: Session = Depends(get_db),
):
    return user_experiences.get_experiences(
        db,
        user_id=user_id,
        business_id=business_id,
        states=state,  # note that the query parameter is called state
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to,
        page=page,
        page_size=page_size,
    )


@router.put("/{id}/assign", response_model=UserExperience)
async def assign_experience(
    id: int, assignmment: ExperienceAssignment, db: Session = Depends(get_db)
):
    return user_experiences.assign(
        db,
        experience_id=id,
        department_id=assignmment.department_id,
        role_id=assignmment.role_id,
        user_id=assignmment.user_id,
    )


@router.put("/{id}/accept", response_model=UserExperience)
async def accept_assignment(
    id: int, acceptance: AssignmentAcceptance, db: Session = Depends(get_db)
):
    return user_experiences.accept(
        db,
        experience_id=id,
        department_id=acceptance.department_id,
        role_id=acceptance.role_id,
        user_id=acceptance.user_id,
    )


@router.put("/{id}/decline", response_model=UserExperience)
async def decline_assignment(id: int, db: Session = Depends(get_db)):
    return user_experiences.decline(db, experience_id=id)


@router.put("/{id}/unassign", response_model=UserExperience)
async def unassign(id: int, db: Session = Depends(get_db)):
    return user_experiences.unassign(db, experience_id=id)


@router.put("/{id}/check-out", response_model=UserExperience)
async def check_out(id: int, db: Session = Depends(get_db)):
    return user_experiences.check_out(db, experience_id=id)
