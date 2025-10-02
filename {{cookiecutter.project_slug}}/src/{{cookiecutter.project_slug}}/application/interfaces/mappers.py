from typing import Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity


class DtoEntityMapperProtocol(Protocol):
    """Protocol for Application layer mapper (Domain Entity <-> Application DTO)."""

    def to_dto(self, entity: ArtifactEntity) -> ArtifactDTO: ...

    def to_entity(self, dto: ArtifactDTO) -> ArtifactEntity: ...

    def to_notification_dto(
        self, entity: ArtifactEntity
    ) -> ArtifactAdmissionNotificationDTO: ...

    def to_publication_dto(
        self, entity: ArtifactEntity
    ) -> ArtifactCatalogPublicationDTO: ...
