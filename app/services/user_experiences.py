from datetime import datetime

from sqlalchemy.orm import Session
from statemachine.exceptions import TransitionNotAllowed

from app import models
from app.internal.user_experience import UserExperienceMachine
from app.services.exceptions import NotFoundException, UserExperienceException


def check_in(db: Session, *, user_id: int, business_id: int):
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise NotFoundException(f"User {user_id} not found.")
    if (
        not db.query(models.Business)
        .filter(models.Business.id == business_id)
        .first()
    ):
        raise NotFoundException(f"Business {business_id} not found.")
    if (
        running_experience := db.query(models.UserExperience)
        .filter(
            models.UserExperience.user_id == user_id,
            models.UserExperience.business_id == business_id,
            models.UserExperience.state != "checked_out",
        )
        .first()
    ):
        raise UserExperienceException(
            f"User experience {running_experience.id} is already in progress."
        )
    machine = UserExperienceMachine(
        models.UserExperience(user_id=user_id, business_id=business_id)
    )
    machine.check_in()
    new_experience = machine.model
    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)
    return new_experience


def get_experience(db: Session, experience_id: int):
    return db.get(models.UserExperience, experience_id)


def get_diagram(db: Session, experience_id: int):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    return machine._graph().create_svg()


def get_experiences(
    db: Session,
    *,
    user_id: int,
    business_id: int,
    states: list[str],
    created_from: datetime,
    created_to: datetime,
    updated_from: datetime,
    updated_to: datetime,
    page: int,
    page_size: int,
):
    query = db.query(models.UserExperience)
    if user_id is not None:
        query = query.filter(models.UserExperience.user_id == user_id)
    if business_id is not None:
        query = query.filter(models.UserExperience.business_id == business_id)
    if states is not None:
        query = query.filter(models.UserExperience.state.in_(states))
    if created_from is not None:
        query = query.filter(models.UserExperience.created_at >= created_from)
    if created_to is not None:
        query = query.filter(models.UserExperience.created_at <= created_to)
    if updated_from is not None:
        query = query.filter(models.UserExperience.updated_at >= updated_from)
    if updated_to is not None:
        query = query.filter(models.UserExperience.updated_at <= updated_to)

    query = query.order_by(models.UserExperience.created_at.desc())

    return query.offset((page - 1) * page_size).limit(page_size).all()


def assign(
    db: Session,
    *,
    experience_id: int,
    department_id: int,
    role_id: int,
    user_id: int,
):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    try:
        machine.assign(department_id, role_id, user_id)
    except TransitionNotAllowed as e:
        raise UserExperienceException(e)
    db.commit()
    db.refresh(experience)
    return experience


def accept(
    db: Session,
    *,
    experience_id: int,
    department_id: int,
    role_id: int,
    user_id: int,
):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    try:
        machine.accept(department_id, role_id, user_id)
    except TransitionNotAllowed as e:
        raise UserExperienceException(e)
    db.commit()
    db.refresh(experience)
    return experience


def decline(db: Session, *, experience_id: int):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    try:
        machine.decline()
    except TransitionNotAllowed as e:
        raise UserExperienceException(e)
    db.commit()
    db.refresh(experience)
    return experience


def unassign(db: Session, *, experience_id: int):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    try:
        machine.unassign()
    except TransitionNotAllowed as e:
        raise UserExperienceException(e)
    db.commit()
    db.refresh(experience)
    return experience


def check_out(db: Session, *, experience_id: int):
    experience = db.get(models.UserExperience, experience_id)
    if not experience:
        raise NotFoundException(f"Experience {experience_id} not found.")
    machine = UserExperienceMachine(experience)
    try:
        machine.check_out()
    except TransitionNotAllowed as e:
        raise UserExperienceException(e)
    db.commit()
    db.refresh(experience)
    return experience
