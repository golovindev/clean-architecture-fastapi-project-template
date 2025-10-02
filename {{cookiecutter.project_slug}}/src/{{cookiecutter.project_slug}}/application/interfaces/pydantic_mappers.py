from typing import Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)
from {{cookiecutter.project_slug}}.infrastructures.dtos.artifact import (
    ArtifactAdmissionNotificationPydanticDTO,
    ArtifactCatalogPublicationPydanticDTO,
    ArtifactPydanticDTO,
)


class PydanticMapperProtocol(Protocol):
    """Protocol for converting Application DTOs to/from Pydantic models.

    This interface is used by Infrastructure components (HTTP clients, message brokers)
    that need to work with Pydantic models for external communication.
    """

    def to_pydantic_dto(self, dto: ArtifactDTO) -> ArtifactPydanticDTO:
        """Convert Application DTO to Pydantic DTO."""
        ...

    def from_pydantic_dto(self, pydantic_dto: ArtifactPydanticDTO) -> ArtifactDTO:
        """Convert Pydantic DTO to Application DTO."""
        ...

    def to_admission_notification_pydantic(
        self, dto: ArtifactAdmissionNotificationDTO
    ) -> ArtifactAdmissionNotificationPydanticDTO:
        """Convert notification DTO to Pydantic format for message broker."""
        ...

    def to_catalog_publication_pydantic(
        self, dto: ArtifactCatalogPublicationDTO
    ) -> ArtifactCatalogPublicationPydanticDTO:
        """Convert publication DTO to Pydantic format for external API."""
        ...
