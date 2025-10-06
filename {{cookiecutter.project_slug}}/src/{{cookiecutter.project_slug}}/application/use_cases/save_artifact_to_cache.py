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
    cache_client: CacheProtocol
    serialization_mapper: SerializationMapperProtocol

    async def execute(self, artifact_dto: ArtifactDTO) -> None:
        await self.cache_client.set(
            artifact_dto.inventory_id, self.serialization_mapper.to_dict(artifact_dto)
        )
        logger.info("Artifact saved to cache", inventory_id=artifact_dto.inventory_id)
