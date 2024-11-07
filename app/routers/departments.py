from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.departments import (
    Department,
    DepartmentCreate,
    DepartmentList,
    DepartmentUpdate
)
from app.services import departments
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=Department)
async def create_department(req: DepartmentCreate,
                            db: Session = Depends(get_db)):
    department = departments.get_department_by_name_business_id_parent_id(
        db, req.name, req.business_id, req.parent_id)
    if department:
        raise HTTPException(
            status_code=400,
            detail="Department already exists.")
    return departments.create_department(db, req)


@router.put("/{department_id}", response_model=Department)
async def update_department(
    department_id: int,
    department_req: DepartmentUpdate,
    db: Session = Depends(get_db)
     ):
    department = departments.update_department(
        db, department_id, department_req)
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.get("/{department_id}", response_model=Department)
async def read_department(department_id: int, db: Session = Depends(get_db)):
    department = departments.get_department(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found.")
    return department


@router.delete("/{department_id}")
async def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = departments.get_department(db, department_id)
    if department:
        departments.delete_department(db, department_id)
    else:
        raise HTTPException(status_code=404, detail="Department not found.")


@router.get("", response_model=DepartmentList)
async def list_departments(business_id: int, db: Session = Depends(get_db)):
    departments_list = departments.get_departments_by_business_id(
        db, business_id)
    return departments_list
