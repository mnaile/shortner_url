from fastapi import APIRouter
from fastapi.param_functions import Query

from app.schemas.schema import ShortnerUrlData, ShortnerUrlSchema, UrlSchema
from app.services.service import ShortnerUrlService

router = APIRouter()


@router.post("/", response_model=ShortnerUrlSchema)
async def create_shortner_url(data: ShortnerUrlData):
    return await ShortnerUrlService().create_shortner_url(data)


@router.get("/", response_model=UrlSchema)
async def get_url(short_url: str = Query(...)):
    return await ShortnerUrlService().get_url(short_url)
