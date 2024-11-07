from sqlalchemy.orm import Session

import app.services.exceptions as ex
from app import models
from app.schemas import touchpoint_roles


def create(
    db: Session,
    touchpoint_id: int,
    touchpoint_role: touchpoint_roles.TouchpointRoleCreate,
):
    new_touchpoint_role = models.TouchpointRole(
        touchpoint_id=touchpoint_id, **touchpoint_role.model_dump()
    )
    db.add(new_touchpoint_role)
    db.commit()
    db.refresh(new_touchpoint_role)
    return new_touchpoint_role


def delete(db: Session, touchpoint_id: int, touchpoint_role_id: int):
    q = db.query(models.TouchpointRole).filter(
        models.TouchpointRole.id == touchpoint_role_id,
        models.TouchpointRole.touchpoint_id == touchpoint_id,
    )
    if touchpoint_role := q.first():
        db.delete(touchpoint_role)
        db.commit()
    else:
        raise ex.NotFoundException(f"TouchpointRole {id} not found.")


def update(
    db: Session,
    touchpoint_id: int,
    touchpoint_role_id: int,
    updated_touchpoint_role: touchpoint_roles.TouchpointRoleUpdate,
):
    touchpoint_role = (
        db.query(models.TouchpointRole)
        .filter(
            models.TouchpointRole.id == touchpoint_role_id,
            models.TouchpointRole.touchpoint_id == touchpoint_id,
        )
        .first()
    )
    if touchpoint_role:
        db.query(models.TouchpointRole).filter(
            models.TouchpointRole.id == touchpoint_role_id,
            models.TouchpointRole.touchpoint_id == touchpoint_id,
        ).update(updated_touchpoint_role.model_dump())
        db.commit()
        db.refresh(touchpoint_role)
        return touchpoint_role
