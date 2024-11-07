from sqlalchemy.orm import Session

from app import models
from app.schemas.preference_links import PreferenceSurveyBase


def get_preference_links(db: Session, business_id: int):
    preference = db.query(models.PreferenceSurvey).filter(
        models.PreferenceSurvey.business_id == business_id
    ).all()

    return preference


def create_preference_link(db: Session, preference: PreferenceSurveyBase):
    db_preference = models.PreferenceSurvey(
        heading=preference.heading,
        subheading=preference.subheading,
        slug=preference.slug,
        image_url=preference.image_url,
        preference_list=preference.preference_list,
        business_id=preference.business_id
    )

    db.add(db_preference)
    db.commit()
    db.refresh(db_preference)
    return db_preference


def get_preference_link(db: Session, id: int):
    preference = db.query(models.PreferenceSurvey).filter(
        models.PreferenceSurvey.id == id
    ).first()

    return preference


def delete_preference(db: Session, preference_link_id: int):
    db_preference = get_preference_link(db, preference_link_id)
    if db_preference:
        db.delete(db_preference)
        db.commit()
        return db_preference


def update_preference_link(
        db: Session,
        preference_link_id: int,
        preference: PreferenceSurveyBase
):
    db_preference = get_preference_link(db, preference_link_id)
    if db_preference:
        db_preference.heading = preference.heading
        db_preference.subheading = preference.subheading
        db_preference.slug = preference.slug
        db_preference.image_url = preference.image_url
        db_preference.preference_list = preference.preference_list
        db_preference.business_id = preference.business_id
        db.commit()
        db.refresh(db_preference)
        return db_preference


def get_preference_links_by_slug(db: Session, slug: str):
    preference = db.query(models.PreferenceSurvey).filter(
        models.PreferenceSurvey.slug == slug
    ).first()

    return preference
