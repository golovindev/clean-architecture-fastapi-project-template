from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from {{cookiecutter.project_slug}}.application.use_cases.get_artifact import GetArtifactUseCase
from {{cookiecutter.project_slug}}.presentation.api.rest.v1.schemas import ArtifactResponse

router = APIRouter(prefix="/v1/artifacts", tags=["Artifacts"])


@router.get(
    "/{inventory_id}",
    response_model=ArtifactResponse,
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
    use_case: FromDishka[GetArtifactUseCase],
) -> ArtifactResponse:
    try:
        artifact_dto = await use_case.execute(inventory_id)
        return ArtifactResponse.from_dto(artifact_dto)
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
