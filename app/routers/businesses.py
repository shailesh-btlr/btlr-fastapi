from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.businesses import Business, BusinessCreate, BusinessUpdate
from app.services import businesses
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=Business)
async def create(req: BusinessCreate, db: Session = Depends(get_db)):
    business = businesses.get_business_by_name(db, req.name)
    if business:
        raise HTTPException(status_code=400, detail="Business already exists.")
    return businesses.create_business(db, req)


@router.get("/{business_id}", response_model=Business)
def read(business_id: int, db: Session = Depends(get_db)):
    business = businesses.get_business(db, business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found.")
    return business


@router.put("/{business_id}", response_model=Business)
def update(
    business_id: int, req: BusinessUpdate, db: Session = Depends(get_db)
):
    business = businesses.get_business(db, business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="Business not found.")
    return businesses.update_business(db, business_id, req)
