from fastapi import APIRouter

from src.presentation.api.rest.v1.controllers.artifact_controller import (
    router as artifact_router,
)

api_v1_router = APIRouter()
api_v1_router.include_router(artifact_router)
