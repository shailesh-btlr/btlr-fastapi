
from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.preference_links import (
    PreferenceSurvey,
    PreferenceSurveyBase,
    PreferenceSurveyList
)
from app.services import preference_links

router = APIRouter()


@router.post("", response_model=PreferenceSurvey)
def create_preference_link(
    preference: PreferenceSurveyBase,
    db: Session = Depends(get_db)
):
    if preference_links.get_preference_links_by_slug(db, preference.slug):
        raise HTTPException(
            status_code=400,
            detail="Slug already exists"
        )
    return preference_links.create_preference_link(db, preference=preference)


@router.get("", response_model=PreferenceSurveyList)
def read_preference_links_by_business_id(
    business_id: int,
    db: Session = Depends(get_db)
):
    db_preferences = preference_links.get_preference_links(db, business_id)
    return db_preferences


@router.get("/slug/{slug}", response_model=PreferenceSurvey)
def read_preference_links_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    db_preferences = preference_links.get_preference_links_by_slug(db, slug)
    if not db_preferences:
        raise HTTPException(
            status_code=404,
            detail="Preference Link not found"
        )
    return db_preferences


@router.get("/{preference_link_id}", response_model=PreferenceSurvey)
def read_preference_link_by_id(
    preference_link_id: int,
    db: Session = Depends(get_db)
):
    db_preference = preference_links.get_preference_link(
        db,
        preference_link_id
    )
    if not db_preference:
        raise HTTPException(
            status_code=404,
            detail="Preference Link not found"
        )
    return db_preference


@router.delete("/{preference_link_id}")
def delete_preference_link(
    preference_link_id: int,
    db: Session = Depends(get_db)
):
    db_preference = preference_links.get_preference_link(
        db,
        preference_link_id
    )
    if db_preference is None:
        raise HTTPException(
            status_code=404,
            detail="Preference Link not found"
        )

    preference_links.delete_preference(db, preference_link_id)


@router.put("/{preference_link_id}", response_model=PreferenceSurvey)
def update_preference_link(
    preference_link_id: int,
    preference: PreferenceSurveyBase,
    db: Session = Depends(get_db)
):
    db_preference = preference_links.get_preference_link(
        db,
        preference_link_id
    )
    if db_preference is None:
        raise HTTPException(status_code=404, detail="Preference not found")

    return preference_links.update_preference_link(
        db,
        preference_link_id,
        preference
    )
