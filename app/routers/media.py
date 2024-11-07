from fastapi import APIRouter

from app.services.media import generate_signed_url
from app.schemas.media import Image

router = APIRouter()


@router.post("/get-upload-url", response_model=str)
async def get_upload_url(image: Image):
    return generate_signed_url(image.name, image.format)
