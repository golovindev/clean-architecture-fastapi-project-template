from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

import structlog

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
)
from {{cookiecutter.project_slug}}.application.interfaces.http_clients import ExternalMuseumAPIProtocol

if TYPE_CHECKING:
    from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class FetchArtifactFromMuseumAPIUseCase:
    """
    Use case for fetching an artifact from an external museum API.
    """

    museum_api_client: ExternalMuseumAPIProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO:
        """
        Executes the use case to fetch an artifact.

        Args:
            inventory_id: The ID of the artifact to fetch.

        Returns:
            An ArtifactDTO representing the fetched artifact.

        Raises:
            ArtifactNotFoundError: If the artifact is not found in the external API.
            FailedFetchArtifactMuseumAPIException: If fetching the artifact fails due to other reasons.
        """
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )
        logger.info(
            "Artifact not found locally, fetching from external museum API...",
            inventory_id=inventory_id_str,
        )
        try:
            artifact_dto = await self.museum_api_client.fetch_artifact(inventory_id)
            logger.info("Artifact fetched from museum API", inventory_id=inventory_id_str)
            return artifact_dto
        except ArtifactNotFoundError as e:
            logger.error(
                "Artifact not found in external museum API",
                inventory_id=inventory_id_str,
                error=str(e),
            )
            raise
        except Exception as e:
            logger.exception(
                "Failed to fetch artifact from external museum API",
                inventory_id=inventory_id_str,
                error=str(e),
            )
            raise FailedFetchArtifactMuseumAPIException(
                "Could not fetch artifact from external service", str(e)
            ) from e
