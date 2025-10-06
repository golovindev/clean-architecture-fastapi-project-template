from dataclasses import dataclass
from typing import TYPE_CHECKING

import structlog

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.application.interfaces.mappers import DtoEntityMapperProtocol
from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol

if TYPE_CHECKING:
    from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SaveArtifactToRepoUseCase:
    uow: UnitOfWorkProtocol
    artifact_mapper: DtoEntityMapperProtocol

    async def execute(self, artifact_dto: ArtifactDTO) -> None:
        async with self.uow:
            artifact_entity = self.artifact_mapper.to_entity(artifact_dto)
            await self.uow.repository.save(artifact_entity)
        logger.info(
            "Artifact saved to repository", inventory_id=artifact_dto.inventory_id
        )
