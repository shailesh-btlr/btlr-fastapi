from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.employees import Employee, EmployeeCreate, EmployeeList
from app.schemas.employee_functions import EmployeeFunctionPopulatedList
from app.services import employees, users
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=Employee)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_user = users.get_user(db, employee.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    db_employee = employees.get_employee_by_business_and_user_id(
        db,
        employee.business_id,
        employee.user_id
    )
    if db_employee:
        raise HTTPException(status_code=400, detail="Employee already exists.")
    return employees.create_employee(db, employee)


@router.get("", response_model=EmployeeList)
def read_employee(business_id: int, db: Session = Depends(get_db)):
    employees_list = employees.get_employees_by_business_id(db, business_id)
    return employees_list


@router.get(
        "/{employee_id}/functions",
        response_model=EmployeeFunctionPopulatedList
)
async def read_employee_functions(
    employee_id: int,
    db: Session = Depends(get_db)
):
    db_employee = employees.get_employee_by_id(db, employee_id)
    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    db_employee_functions = employees.get_employee_functions(
        db, employee_id
    )

    return db_employee_functions


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = employees.get_employee_by_id(db, employee_id)
    if employee:
        employees.delete_employee(db, employee_id)
    else:
        raise HTTPException(status_code=404, detail="Employee not found.")
