from app import models
from app.schemas import employee_functions
from sqlalchemy.orm import Session


def create_employee_function(
        db: Session, employee_function:
        employee_functions.EmployeeFunctionCreate):
    employee_function = models.EmployeeFunction(
        **employee_function.model_dump()
        )
    db.add(employee_function)
    db.commit()
    db.refresh(employee_function)
    return employee_function


def get_employee_function(db: Session, employee_function_id: int):
    return db.query(models.EmployeeFunction).filter(
        models.EmployeeFunction.id == employee_function_id).first()


def get_emp_by_emp_role_and_dept_id(
        db: Session,
        employee_id: int,
        role_id: int,
        department_id: int):
    return db.query(models.EmployeeFunction).filter(
        models.EmployeeFunction.employee_id == employee_id,
        models.EmployeeFunction.role_id == role_id,
        models.EmployeeFunction.department_id == department_id
        ).first()


def update_employee_function(
        db: Session,
        employee_function_id: int,
        updated_employee_function:
        employee_functions.EmployeeFunctionUpdate
        ):
    employee_function = db.query(models.EmployeeFunction).filter(
        models.EmployeeFunction.id == employee_function_id).first()
    if employee_function:
        db.query(
            models.EmployeeFunction).filter(
            models.EmployeeFunction.id == employee_function_id).update(
            updated_employee_function.model_dump()
            )
        db.commit()
        db.refresh(employee_function)
    return employee_function


def delete_employee_function(db: Session, employee_function_id: int):
    employee_function = db.query(models.EmployeeFunction).filter(
        models.EmployeeFunction.id == employee_function_id).first()
    if employee_function:
        db.delete(employee_function)
        db.commit()
