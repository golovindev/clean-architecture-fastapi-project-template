from abc import abstractmethod
from typing import Any, Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)


class PydanticMapperProtocol(Protocol):
    """Protocol for converting Application DTOs to/from Pydantic models.

    This interface is used by Infrastructure components (HTTP clients, message brokers)
    that need to work with Pydantic models for external communication.

    Note: Return types use Any to avoid importing Infrastructure layer types,
    maintaining Clean Architecture dependency rules (Application should not depend on Infrastructure).
    """

    @abstractmethod
    def to_pydantic_dto(self, dto: ArtifactDTO) -> Any:
        """Convert Application DTO to Pydantic DTO.

        Returns:
            Pydantic model (ArtifactPydanticDTO) for external API communication.
        """
        ...

    @abstractmethod
    def from_pydantic_dto(self, pydantic_dto: Any) -> ArtifactDTO:
        """Convert Pydantic DTO to Application DTO.

        Args:
            pydantic_dto: Pydantic model (ArtifactPydanticDTO) from external API.

        Returns:
            Application DTO for use in business logic.
        """
        ...

    @abstractmethod
    def to_admission_notification_pydantic(
        self, dto: ArtifactAdmissionNotificationDTO
    ) -> Any:
        """Convert notification DTO to Pydantic format for message broker.

        Returns:
            Pydantic model (ArtifactAdmissionNotificationPydanticDTO).
        """
        ...

    @abstractmethod
    def to_catalog_publication_pydantic(
        self, dto: ArtifactCatalogPublicationDTO
    ) -> Any:
        """Convert publication DTO to Pydantic format for external API.

        Returns:
            Pydantic model (ArtifactCatalogPublicationPydanticDTO).
        """
        ...
