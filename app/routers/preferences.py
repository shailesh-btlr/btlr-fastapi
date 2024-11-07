from app.config import settings
from fastapi import APIRouter, HTTPException
from app.schemas.preferences import (
    PreferenceAdd,
    PreferenceTree,
    PreferenceTreeAdd,
)
from app.services import graph


router = APIRouter()


def new_graph():
    return graph.PreferenceGraph(
        settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD
    )


@router.post("")
async def add_preference_to_user(req: PreferenceAdd):
    with new_graph() as g:
        g.add_preference_to_user(req.user_id, req.parent_id, req.name)
        return 201


@router.get("/tree", response_model=PreferenceTree)
def get_preference_tree(user_id) -> PreferenceTree:
    with new_graph() as g:
        tree = g.get_preference_tree_for_user(user_id)
        if tree:
            return tree
        else:
            raise HTTPException(status_code=404, detail="Tree not found.")


@router.post("/tree")
def add_preferences_tree(req: PreferenceTreeAdd):
    with new_graph() as g:
        g.add_preference_tree_to_user(req.tree.model_dump(), req.user_id)
        return 201


@router.delete("")
def unlink_preference_from_user(user_id, preference_id):
    with new_graph() as g:
        g.unlink_preference_from_user(user_id, preference_id)
        return 200
