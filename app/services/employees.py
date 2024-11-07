
from app import models
from app.schemas import employees
from sqlalchemy.orm import Session


def create_employee(db: Session, employee: employees.EmployeeCreate):
    new_employee = models.Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


def get_employee_by_business_and_user_id(
        db: Session,
        business_id: int,
        user_id: int
):
    return (
        db.query(models.Employee).filter(
            models.Employee.business_id == business_id,
            models.Employee.user_id == user_id).first()
    )


def get_employees_by_business_id(db: Session, business_id: int):
    return (
        db.query(models.Employee)
        .filter(models.Employee.business_id == business_id)
        .all()
    )


def get_employee_by_id(db: Session, id: int):
    return (
        db.query(models.Employee)
        .filter(models.Employee.id == id)
        .first()
    )


def delete_employee(db: Session, employee_id):
    employee = db.query(
        models.Employee).filter(
            models.Employee.id == employee_id
        ).first()
    if employee:
        db.delete(employee)
        db.commit()


def get_employee_functions(db: Session, employee_id: int):
    return db.query(models.EmployeeFunction).filter(
        models.EmployeeFunction.employee_id == employee_id,
        ).all()
