from sqlalchemy.orm import Session

from app.config import settings
from app.schemas.insights import DebugInsight
from app.services import (businesses, chat, flowise, gpt, graph, touchpoints,
                          zep)


def generate_insight(
    db: Session, user_id: int, touchpoint_id: int, role_id: int, max_tokens: int
) -> DebugInsight:

    touchpoint = touchpoints.read(db, touchpoint_id)

    business = businesses.get_business(db, touchpoint.business_id)

    touchpoint_role = next(
        tpr for tpr in touchpoint.touchpoint_roles if tpr.role_id == role_id
    )

    touchpoint_cluster_names = [
        cluster.name for cluster in touchpoint.touchpoint_clusters
    ]

    question = (
        f"Touchpoint: {touchpoint.name} "
        f"Description: {touchpoint.description} "
        f"Department: {touchpoint.department.name} "
        f"Service Role: {touchpoint_role.role.name} "
        f"Preference theme: {', '.join(touchpoint_cluster_names)} "
    )

    recommendation = flowise.query(
        dict(
            question=question,
            overrideConfig=dict(
                sessionId=zep.to_zep_username(chat.to_chat_username(user_id)),
                zepCollection=zep.to_zep_business_name(business.id),
            ),
        )
    )

    return dict(
        prompt=question,
        recommendation=recommendation,
        task_list=touchpoint_role.role.task_list,
    )
