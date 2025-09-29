from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, Literal
from uuid import UUID

from src.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from src.application.interfaces.repositories import ArtifactRepositoryProtocol

if TYPE_CHECKING:
    from src.domain.entities.artifact import ArtifactEntity

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactUseCase:
    repository: ArtifactRepositoryProtocol
    museum_api_client: ExternalMuseumAPIProtocol
    catalog_api_client: PublicCatalogAPIProtocol
    message_broker: MessageBrokerPublisherProtocol
    artifact_mapper: DtoEntityMapperProtocol
    cache_client: CacheProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )

        cached_artifact: ArtifactDTO | None = await self.cache_client.get(
            inventory_id_str
        )
        if cached_artifact:
            return ArtifactDTO.model_validate(cached_artifact)

        artifact_entity: (
            ArtifactEntity | None
        ) = await self.repository.get_by_inventory_id(inventory_id_str)
        if artifact_entity:
            artifact_dto = self.artifact_mapper.to_dto(artifact_entity)
            await self.cache_client.set(
                inventory_id_str, artifact_dto.model_dump_json()
            )
            return artifact_dto

        logger.info(
            "Artifact not found locally, fetching from external museum API...",
            extra={"inventory_id": inventory_id_str},
        )
        try:
            artifact_dto = await self.museum_api_client.fetch_artifact(inventory_id)
        except ArtifactNotFoundError as e:
            logger.error(
                "Artifact not found in external museum API",
                extra={"inventory_id": inventory_id_str, "error": str(e)},
            )
            raise
        except Exception as e:
            logger.exception(
                "Failed to fetch artifact from external museum API",
                extra={"inventory_id": inventory_id_str, "error": str(e)},
            )
            raise FailedFetchArtifactMuseumAPIException(
                "Could not fetch artifact from external service", str(e)
            ) from e

        artifact_entity = self.artifact_mapper.to_entity(artifact_dto)
        await self.repository.save(artifact_entity)
        await self.cache_client.set(inventory_id_str, artifact_dto.model_dump_json())

        try:
            notification_dto = ArtifactAdmissionNotificationDTO(
                inventory_id=artifact_entity.inventory_id,
                name=artifact_entity.name,
                acquisition_date=artifact_entity.acquisition_date,
                department=artifact_entity.department,
            )
            await self.message_broker.publish_new_artifact(notification_dto)
            logger.info(
                "Published new artifact event to message broker",
                extra={"inventory_id": inventory_id_str},
            )
        except Exception as e:
            logger.warning(
                "Failed to publish artifact notification to message broker (non-critical)",
                extra={"inventory_id": inventory_id_str, "error": str(e)},
            )
            raise FailedPublishArtifactMessageBrokerException(
                "Failed to publish message to broker", str(e)
            ) from e

        try:
            publication_dto = ArtifactCatalogPublicationDTO(
                inventory_id=artifact_entity.inventory_id,
                name=artifact_entity.name,
                era=EraDTO(value=self._validate_era(artifact_entity.era.value)),
                material=MaterialDTO(
                    value=self._validate_material(artifact_entity.material.value)
                ),
                description=artifact_entity.description,
            )
            public_id: str = await self.catalog_api_client.publish_artifact(
                publication_dto
            )
            logger.info(
                "Artifact published to public catalog",
                extra={"inventory_id": inventory_id_str, "public_id": public_id},
            )
        except Exception as e:
            logger.exception(
                "Failed to publish artifact to catalog",
                extra={"inventory_id": inventory_id_str, "error": str(e)},
            )
            raise FailedPublishArtifactInCatalogException(
                "Could not publish artifact to catalog", str(e)
            ) from e

        logger.info(
            "Artifact successfully fetched and processed",
            extra={"inventory_id": inventory_id_str},
        )
        return artifact_dto

    def _validate_era(
        self, value: str
    ) -> Literal[
        "paleolithic",
        "neolithic",
        "bronze_age",
        "iron_age",
        "antiquity",
        "middle_ages",
        "modern",
    ]:
        allowed = {
            "paleolithic",
            "neolithic",
            "bronze_age",
            "iron_age",
            "antiquity",
            "middle_ages",
            "modern",
        }
        if value not in allowed:
            raise ValueError(f"Invalid era value: {value}")
        return value  # type: ignore[return-value]

    def _validate_material(
        self, value: str
    ) -> Literal[
        "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
    ]:
        allowed = {
            "ceramic",
            "metal",
            "stone",
            "glass",
            "bone",
            "wood",
            "textile",
            "other",
        }
        if value not in allowed:
            raise ValueError(f"Invalid material value: {value}")
        return value  # type: ignore[return-value]
