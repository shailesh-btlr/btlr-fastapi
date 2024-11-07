from fastapi import APIRouter

from app.schemas.opa import OpaInput
from app.services import opa

router = APIRouter()


@router.post("/", response_model=dict)
async def query(input: OpaInput):
    return opa.query(input)
