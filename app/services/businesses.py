from sqlalchemy.orm import Session

from app import models
from app.schemas import businesses
from app.services import zep

# from app.services import graph
# from app.config import settings

def get_business(db: Session, id: int):
    return (
        db.query(models.Business).filter(models.Business.id == id).first()
    )  # noqa E501


def get_business_by_name(db: Session, name: str):
    return (
        db.query(models.Business).filter(models.Business.name == name).first()
    )  # noqa E501


def create_business(db: Session, business: businesses.BusinessCreate):
    new_business = models.Business(name=business.name)
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    zep.create_business_collection(new_business.id)
    # with graph.PreferenceGraph(
    #     settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD
    # ) as g:
    #     g.setup_user(f"b{new_business.id}")
    #     g.close()
    return new_business


def update_business(
    db: Session, business_id: int, updated_business: businesses.BusinessUpdate
):
    business = (
        db.query(models.Business).filter(models.Business.id == business_id).first()
    )
    if business:
        db.query(models.Business).filter(models.Business.id == business_id).update(
            updated_business.model_dump()
        )
        db.commit()
        db.refresh(business)
        return business
