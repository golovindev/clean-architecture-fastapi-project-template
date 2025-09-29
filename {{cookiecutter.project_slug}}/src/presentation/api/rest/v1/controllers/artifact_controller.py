from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from src.application.dtos.artifact import ArtifactDTO
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.use_cases.get_artifact import GetArtifactUseCase

router = APIRouter(prefix="/v1/artifacts", tags=["Artifacts"])


@router.get(
    "/{inventory_id}",
    response_model=ArtifactDTO,
    summary="Get artifact by inventory ID",
    responses={
        200: {"description": "Artifact retrieved successfully"},
        400: {"description": "Bad request (e.g., invalid external API response)"},
        404: {"description": "Artifact not found"},
        500: {"description": "Internal server error"},
        502: {"description": "Failed to notify via message broker"},
    },
)
@inject
async def get_artifact(
    inventory_id: str | UUID,
    use_case: Annotated[GetArtifactUseCase, FromDishka()],
) -> ArtifactDTO:
    try:
        return await use_case.execute(inventory_id)
    except ArtifactNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artifact not found in the system.",
        ) from err
    except FailedFetchArtifactMuseumAPIException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fetch artifact data from the museum API.",
        ) from err
    except FailedPublishArtifactInCatalogException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artifact could not be published in the catalog.",
        ) from err
    except FailedPublishArtifactMessageBrokerException as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to send notification via message broker.",
        ) from err
