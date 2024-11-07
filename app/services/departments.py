from app import models
from app.schemas import departments
from sqlalchemy.orm import Session


def create_department(db: Session, department: departments.DepartmentCreate):
    new_department = models.Department(**department.model_dump())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


def get_department_by_name_business_id_parent_id(db: Session, name: str, 
                                                 business_id: int, 
                                                 parent_id: int):
    return (
        db.query(models.Department).filter(
            models.Department.name == name,
            models.Department.business_id == business_id,
            models.Department.parent_id == parent_id).first()
    )


def get_department(db: Session, department_id: int):
    return (
        db.query(models.Department).filter(
            models.Department.id == department_id).first()
    )


def delete_department(db: Session, department_id: int):
    department = db.query(models.Department).filter(
        models.Department.id == department_id).first()
    if department:
        db.delete(department)
        db.commit()


def get_departments_by_business_id(db: Session, business_id: int):
    return (
        db.query(models.Department).filter(
            models.Department.business_id == business_id).all()
    )


def update_department(
        db: Session, department_id: int,
        updated_department: departments.DepartmentUpdate):
    department = db.query(models.Department).filter(
        models.Department.id == department_id).first()
    if department:
        db.query(models.Department).filter(
            models.Department.id == department_id).update(
                updated_department.model_dump())
        db.commit()
        db.refresh(department)
        return department