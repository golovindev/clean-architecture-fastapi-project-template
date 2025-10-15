from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Path

from {{cookiecutter.project_slug}}.application.use_cases.process_artifact import ProcessArtifactUseCase
from {{cookiecutter.project_slug}}.presentation.api.rest.v1.mappers.artifact_mapper import ArtifactPresentationMapper
from {{cookiecutter.project_slug}}.presentation.api.rest.v1.schemas import ArtifactResponseSchema

router = APIRouter(prefix="/v1/artifacts", tags=["Artifacts"])


@router.get(
    "/{inventory_id}",
    response_model=ArtifactResponseSchema,
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
    inventory_id: UUID = Path(..., description="Artifact UUID"),
    use_case: FromDishka[ProcessArtifactUseCase] = None,
    presentation_mapper: FromDishka[ArtifactPresentationMapper] = None,
) -> ArtifactResponseSchema:
    artifact_dto = await use_case(str(inventory_id))
    return presentation_mapper.to_response(artifact_dto)
