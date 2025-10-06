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
class GetArtifactFromCacheUseCase:
    cache_client: CacheProtocol
    serialization_mapper: SerializationMapperProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO | None:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )

        cached_artifact_data: dict | None = await self.cache_client.get(inventory_id_str)
        if cached_artifact_data:
            logger.info("Artifact found in cache", inventory_id=inventory_id_str)
            return self.serialization_mapper.from_dict(cached_artifact_data)
        logger.info("Artifact not found in cache", inventory_id=inventory_id_str)
        return None
