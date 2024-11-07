from sqlalchemy.orm import Session

import app.services.exceptions as ex
from app import models
from app.schemas import touchpoints


def create(db: Session, touchpoint: touchpoints.TouchpointCreate):
    new_touchpoint = models.Touchpoint(**touchpoint.model_dump())
    db.add(new_touchpoint)
    db.commit()
    db.refresh(new_touchpoint)
    return new_touchpoint


def read(db: Session, id: int):
    q = db.query(models.Touchpoint).filter(models.Touchpoint.id == id)
    if touchpoint := q.first():
        return touchpoint
    else:
        raise ex.NotFoundException(f"Touchpoint {id} not found.")


def read_all(db: Session, business_id: int):
    return (
        db.query(models.Touchpoint)
        .filter(models.Touchpoint.business_id == business_id)
        .all()
    )


def update(
    db: Session, id: int, updated_touchpoint: touchpoints.TouchpointUpdate
):
    q = db.query(models.Touchpoint).filter(models.Touchpoint.id == id)
    if touchpoint := q.first():
        q.update(updated_touchpoint.model_dump())
        db.commit()
        db.refresh(touchpoint)
        return touchpoint
    else:
        raise ex.NotFoundException(f"Touchpoint {id} not found.")


def delete(db: Session, id: int):
    q = db.query(models.Touchpoint).filter(models.Touchpoint.id == id)
    if touchpoint := q.first():
        db.delete(touchpoint)
        db.commit()
    else:
        raise ex.NotFoundException(f"Touchpoint {id} not found.")
