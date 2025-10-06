from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

import structlog

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.application.interfaces.cache import CacheProtocol
from {{cookiecutter.project_slug}}.application.interfaces.serialization import SerializationMapperProtocol

if TYPE_CHECKING:
    from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveArtifactToCacheUseCase:
    """
    Use case for saving an artifact to the cache.
    """

    cache_client: CacheProtocol
    serialization_mapper: SerializationMapperProtocol

    async def execute(self, inventory_id: str | UUID, artifact_dto: ArtifactDTO) -> None:
        """
        Executes the use case to save an artifact to the cache.

        Args:
            inventory_id: The ID of the artifact to save.
            artifact_dto: The ArtifactDTO to save.
        """
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )
        await self.cache_client.set(
            inventory_id_str, self.serialization_mapper.to_dict(artifact_dto)
        )
        logger.info("Artifact saved to cache", inventory_id=inventory_id_str)
