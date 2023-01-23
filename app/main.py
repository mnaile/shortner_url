from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from app.config import settings
from app.controllers.controller import router
from app.data.model import db  # noqa

app = FastAPI(docs_url=settings.SWAGGER_URL, redoc_url=settings.REDOC_URL)

if not settings.TESTING:
    db.init_app(app)

def modify_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Interview Task",
        version=settings.API_VERSION,
        description="",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


cors_origins = [i.strip() for i in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.BASE_URL)
