from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

import structlog

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from {{cookiecutter.project_slug}}.application.interfaces.cache import CacheProtocol
from {{cookiecutter.project_slug}}.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from {{cookiecutter.project_slug}}.application.interfaces.mappers import DtoEntityMapperProtocol
from {{cookiecutter.project_slug}}.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol

if TYPE_CHECKING:
    from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactUseCase:
    uow: UnitOfWorkProtocol
    museum_api_client: ExternalMuseumAPIProtocol
    catalog_api_client: PublicCatalogAPIProtocol
    message_broker: MessageBrokerPublisherProtocol
    artifact_mapper: DtoEntityMapperProtocol
    cache_client: CacheProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )

        cached_artifact_data: dict | None = await self.cache_client.get(inventory_id_str)
        if cached_artifact_data:
            return self.artifact_mapper.from_dict(cached_artifact_data)

        artifact_entity: (
            ArtifactEntity | None
        ) = await self.uow.repository.get_by_inventory_id(inventory_id_str)
        if artifact_entity:
            artifact_dto = self.artifact_mapper.to_dto(artifact_entity)
            await self.cache_client.set(
                inventory_id_str, self.artifact_mapper.to_dict(artifact_dto)
            )
            return artifact_dto

        logger.info(
            "Artifact not found locally, fetching from external museum API...",
            inventory_id=inventory_id_str,
        )
        try:
            artifact_dto = await self.museum_api_client.fetch_artifact(inventory_id)
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

        async with self.uow:
            artifact_entity = self.artifact_mapper.to_entity(artifact_dto)
            await self.uow.repository.save(artifact_entity)
            await self.cache_client.set(inventory_id_str, self.artifact_mapper.to_dict(artifact_dto))

        try:
            notification_dto = self.artifact_mapper.to_notification_dto(
                artifact_entity
            )
            await self.message_broker.publish_new_artifact(notification_dto)
            logger.info(
                "Published new artifact event to message broker",
                inventory_id=inventory_id_str,
            )
        except Exception as e:
            logger.warning(
                "Failed to publish artifact notification to message broker (non-critical)",
                inventory_id=inventory_id_str,
                error=str(e),
            )
            raise FailedPublishArtifactMessageBrokerException(
                "Failed to publish message to broker", str(e)
            ) from e

        try:
            publication_dto = self.artifact_mapper.to_publication_dto(artifact_entity)
            public_id: str = await self.catalog_api_client.publish_artifact(
                publication_dto
            )
            logger.info(
                "Artifact published to public catalog",
                inventory_id=inventory_id_str,
                public_id=public_id,
            )
        except Exception as e:
            logger.exception(
                "Failed to publish artifact to catalog",
                inventory_id=inventory_id_str,
                error=str(e),
            )
            raise FailedPublishArtifactInCatalogException(
                "Could not publish artifact to catalog", str(e)
            ) from e

        logger.info(
            "Artifact successfully fetched and processed",
            inventory_id=inventory_id_str,
        )
        return artifact_dto
