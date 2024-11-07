from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.touchpoint_clusters import (
    TouchpointCluster,
    TouchpointClusterCreate,
)
from app.schemas.touchpoint_roles import (
    TouchpointRole,
    TouchpointRoleCreate,
    TouchpointRoleUpdate,
)
from app.schemas.touchpoints import (
    Touchpoint,
    TouchpointCreate,
    TouchpointList,
    TouchpointUpdate,
)
from app.services import touchpoint_clusters, touchpoint_roles, touchpoints

router = APIRouter()


@router.post("", response_model=Touchpoint, status_code=status.HTTP_201_CREATED)
def create(req: TouchpointCreate, db: Session = Depends(get_db)):
    return touchpoints.create(db, req)


@router.get(
    "/{touchpoint_id}",
    response_model=Touchpoint,
    status_code=status.HTTP_200_OK,
)
def read(touchpoint_id: int, db: Session = Depends(get_db)):
    touchpoint = touchpoints.read(db, touchpoint_id)
    if touchpoint is None:
        raise HTTPException(status_code=404, detail="Touchpoint not found.")
    return touchpoint


@router.get("", response_model=TouchpointList)
def read_all(business_id: int, db: Session = Depends(get_db)):
    return touchpoints.read_all(db, business_id)


@router.put("/{touchpoint_id}", response_model=Touchpoint)
def update(
    touchpoint_id: int, req: TouchpointUpdate, db: Session = Depends(get_db)
):
    touchpoint = touchpoints.update(db, touchpoint_id, req)
    if touchpoint is None:
        raise HTTPException(status_code=404, detail="Touchpoint not found.")
    return touchpoint


@router.delete("/{touchpoint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(touchpoint_id: int, db: Session = Depends(get_db)):
    touchpoints.delete(db, touchpoint_id)


@router.post(
    "/{touchpoint_id}/clusters",
    response_model=TouchpointCluster,
    status_code=status.HTTP_201_CREATED,
)
def create_touchpoint_cluster(
    touchpoint_id: int,
    req: TouchpointClusterCreate,
    db: Session = Depends(get_db),
):
    return touchpoint_clusters.create(db, touchpoint_id, req)


@router.delete(
    "/{touchpoint_id}/clusters/{touchpoint_cluster_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_touchpoint_cluster(
    touchpoint_id: int,
    touchpoint_cluster_id: int,
    db: Session = Depends(get_db),
):
    touchpoint_clusters.delete(db, touchpoint_id, touchpoint_cluster_id)


@router.post(
    "/{touchpoint_id}/roles",
    response_model=TouchpointRole,
    status_code=status.HTTP_201_CREATED,
)
def create_touchpoint_role(
    touchpoint_id: int, req: TouchpointRoleCreate, db: Session = Depends(get_db)
):
    return touchpoint_roles.create(db, touchpoint_id, req)


@router.put(
    "/{touchpoint_id}/roles/{touchpoint_role_id}", response_model=TouchpointRole
)
def update_touchpoint_role(
    touchpoint_id: int,
    touchpoint_role_id: int,
    req: TouchpointRoleUpdate,
    db: Session = Depends(get_db),
):
    touchpoint_role = touchpoint_roles.update(
        db, touchpoint_id, touchpoint_role_id, req
    )
    if touchpoint_role is None:
        raise HTTPException(
            status_code=404, detail="Touchpoint role not found."
        )
    return touchpoint_role


@router.delete(
    "/{touchpoint_id}/roles/{touchpoint_role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_touchpoint_role(
    touchpoint_id: int, touchpoint_role_id: int, db: Session = Depends(get_db)
):
    touchpoint_roles.delete(db, touchpoint_id, touchpoint_role_id)
