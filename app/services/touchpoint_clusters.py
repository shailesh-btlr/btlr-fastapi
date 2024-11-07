from sqlalchemy.orm import Session

import app.services.exceptions as ex
from app import models
from app.schemas import touchpoint_clusters


def create(
    db: Session,
    touchpoint_id: int,
    touchpoint_cluster: touchpoint_clusters.TouchpointClusterCreate,
):
    new_touchpoint_cluster = models.TouchpointCluster(
        touchpoint_id=touchpoint_id, **touchpoint_cluster.model_dump()
    )
    db.add(new_touchpoint_cluster)
    db.commit()
    db.refresh(new_touchpoint_cluster)
    return new_touchpoint_cluster


def delete(db: Session, touchpoint_id: int, touchpoint_cluster_id: int):
    q = (
        db.query(models.TouchpointCluster)
        .filter(
            models.TouchpointCluster.id == touchpoint_cluster_id,
            models.TouchpointCluster.touchpoint_id == touchpoint_id
            )
    )
    if touchpoint_cluster := q.first():
        db.delete(touchpoint_cluster)
        db.commit()
    else:
        raise ex.NotFoundException(f"TouchpointCluster {id} not found.")
