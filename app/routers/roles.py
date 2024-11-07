from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.roles import Role, RoleCreate, RoleUpdate, RoleList
from app.services import roles
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=Role)
async def create_role(req: RoleCreate, db: Session = Depends(get_db)):
    role = roles.get_role_by_name_parent_id_business_id(db, req.name,
                                                        req.parent_id,
                                                        req.business_id)
    if role:
        raise HTTPException(status_code=400, detail="Role already exists.")
    return roles.create_role(db, req)


@router.get("/{role_id}", response_model=Role)
async def read_role(role_id: int, db: Session = Depends(get_db)):
    role = roles.get_role(db, role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.get("", response_model=RoleList)
async def read_all_roles(business_id: int, db: Session = Depends(get_db)):
    all_roles = roles.get_all_roles_business_id(db, business_id)
    return all_roles


@router.put("/{role_id}", response_model=Role)
async def update_role(role_id: int, role: RoleUpdate,
                      db: Session = Depends(get_db)):
    role = roles.update_role(db, role_id, role)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.delete("/{role_id}")
async def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = roles.get_role(db, role_id)
    if role:
        roles.delete_role(db, role_id)
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
