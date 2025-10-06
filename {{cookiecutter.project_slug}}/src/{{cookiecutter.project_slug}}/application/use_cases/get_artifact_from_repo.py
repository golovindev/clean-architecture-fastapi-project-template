from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

import structlog

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.application.interfaces.mappers import DtoEntityMapperProtocol
from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol

if TYPE_CHECKING:
    from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactFromRepoUseCase:
    uow: UnitOfWorkProtocol
    artifact_mapper: DtoEntityMapperProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO | None:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )

        artifact_entity: (
            ArtifactEntity | None
        ) = await self.uow.repository.get_by_inventory_id(inventory_id_str)
        if artifact_entity:
            logger.info("Artifact found in repository", inventory_id=inventory_id_str)
            return self.artifact_mapper.to_dto(artifact_entity)
        logger.info("Artifact not found in repository", inventory_id=inventory_id_str)
        return None
