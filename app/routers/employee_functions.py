from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.employee_functions import (
    EmployeeFunction,
    EmployeeFunctionCreate,
    EmployeeFunctionUpdate,
)
from app.services import employee_functions
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=EmployeeFunctionCreate)
async def create_employee_function(
    employee_function_req: EmployeeFunctionCreate,
    db: Session = Depends(get_db)
):
    employee = employee_functions.get_emp_by_emp_role_and_dept_id(
        db, employee_function_req.employee_id,
        employee_function_req.role_id,
        employee_function_req.department_id)
    if employee:
        raise HTTPException(status_code=400, detail="Employee already exists.")
    return employee_functions.create_employee_function(
        db,
        employee_function_req)


@router.get("/{employee_function_id}", response_model=EmployeeFunction)
async def read_employee_function(
    employee_function_id: int, db: Session = Depends(get_db)
):
    employee_function = employee_functions.get_employee_function(
        db, employee_function_id
    )
    if employee_function is None:
        raise HTTPException(
            status_code=404,
            detail="EmployeeFunction not found."
        )
    return employee_function


@router.put("/{employee_function_id}", response_model=EmployeeFunctionUpdate)
async def update_employee_function(
    employee_function_id: int,
    employee_function_req: EmployeeFunctionUpdate,
    db: Session = Depends(get_db),
):
    employee_function = employee_functions.update_employee_function(
        db, employee_function_id, employee_function_req
    )
    if employee_function is None:
        raise HTTPException(
            status_code=404,
            detail="EmployeeFunction not found."
            )
    return employee_function


@router.delete(
    "/{employee_function_id}"
)
async def delete_employee_function(
    employee_function_id: int, db: Session = Depends(get_db)
):
    employee_function = employee_functions.get_employee_function(
        db, employee_function_id)
    if employee_function:
        employee_functions.delete_employee_function(db, employee_function_id)
    else:
        raise HTTPException(
            status_code=404,
            detail="EmployeeFunction not found."
            )
