from app import models
from app.schemas import roles
from sqlalchemy.orm import Session


def create_role(db: Session, role: roles.RoleCreate):
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def get_role_by_name_parent_id_business_id(db: Session, name: str,
                                           parent_id: int,
                                           business_id: int):
    return db.query(models.Role).filter(
        models.Role.name == name,
        models.Role.parent_id == parent_id,
        models.Role.business_id == business_id
    ).first()


def get_all_roles_business_id(db: Session, business_id: int):
    return db.query(models.Role).filter(
        models.Role.business_id == business_id).all()


def update_role(db: Session, role_id: int, updated_role: roles.RoleUpdate):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role:
        db.query(models.Role).filter(
            models.Role.id == role_id).update(updated_role.model_dump())
        db.commit()
        db.refresh(role)
        return role


def delete_role(db: Session, role_id: int):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
