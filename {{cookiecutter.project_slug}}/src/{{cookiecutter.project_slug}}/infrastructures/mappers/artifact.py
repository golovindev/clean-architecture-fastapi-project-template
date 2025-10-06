from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from {{cookiecutter.project_slug}}.application.interfaces.pydantic_mappers import PydanticMapperProtocol
from {{cookiecutter.project_slug}}.application.interfaces.serialization import SerializationMapperProtocol
from {{cookiecutter.project_slug}}.infrastructures.dtos.artifact import (
    ArtifactAdmissionNotificationPydanticDTO,
    ArtifactCatalogPublicationPydanticDTO,
    ArtifactPydanticDTO,
    EraPydanticDTO,
    MaterialPydanticDTO,
)


@final
@dataclass(frozen=True, slots=True)
class InfrastructureArtifactMapper(PydanticMapperProtocol, SerializationMapperProtocol):
    """Mapper for converting between Application DTOs and Infrastructure Pydantic models.

    This mapper implements both:
    - PydanticMapperProtocol: Conversion to/from Pydantic models for external APIs
    - SerializationMapperProtocol: JSON serialization/deserialization for caching
    """

    def to_pydantic_dto(self, dto: ArtifactDTO) -> ArtifactPydanticDTO:
        """
        Converts an Application ArtifactDTO to an Infrastructure ArtifactPydanticDTO.
        """
        return ArtifactPydanticDTO(
            inventory_id=dto.inventory_id,
            created_at=dto.created_at,
            acquisition_date=dto.acquisition_date,
            name=dto.name,
            department=dto.department,
            era=EraPydanticDTO(value=dto.era.value),
            material=MaterialPydanticDTO(value=dto.material.value),
            description=dto.description,
        )

    def from_pydantic_dto(self, pydantic_dto: ArtifactPydanticDTO) -> ArtifactDTO:
        """
        Converts an Infrastructure ArtifactPydanticDTO to an Application ArtifactDTO.
        """
        return ArtifactDTO(
            inventory_id=pydantic_dto.inventory_id,
            created_at=pydantic_dto.created_at,
            acquisition_date=pydantic_dto.acquisition_date,
            name=pydantic_dto.name,
            department=pydantic_dto.department,
            era=EraDTO(value=pydantic_dto.era.value),
            material=MaterialDTO(value=pydantic_dto.material.value),
            description=pydantic_dto.description,
        )

    def to_admission_notification_pydantic(
        self, dto: ArtifactAdmissionNotificationDTO
    ) -> ArtifactAdmissionNotificationPydanticDTO:
        """
        Converts an ArtifactAdmissionNotificationDTO to an ArtifactAdmissionNotificationPydanticDTO.
        """
        return ArtifactAdmissionNotificationPydanticDTO(
            inventory_id=dto.inventory_id,
            name=dto.name,
            acquisition_date=dto.acquisition_date,
            department=dto.department,
        )

    def to_catalog_publication_pydantic(
        self, dto: ArtifactCatalogPublicationDTO
    ) -> ArtifactCatalogPublicationPydanticDTO:
        """
        Converts an ArtifactCatalogPublicationDTO to an ArtifactCatalogPublicationPydanticDTO.
        """
        return ArtifactCatalogPublicationPydanticDTO(
            inventory_id=dto.inventory_id,
            name=dto.name,
            era=EraPydanticDTO(value=dto.era.value),
            material=MaterialPydanticDTO(value=dto.material.value),
            description=dto.description,
        )

    def to_dict(self, dto: ArtifactDTO) -> dict:
        """
        Converts an Application ArtifactDTO to a dictionary for JSON serialization (e.g., caching).
        """
        return {
            "inventory_id": str(dto.inventory_id),
            "created_at": dto.created_at.isoformat(),
            "acquisition_date": dto.acquisition_date.isoformat(),
            "name": dto.name,
            "department": dto.department,
            "era": {"value": dto.era.value},
            "material": {"value": dto.material.value},
            "description": dto.description,
        }

    def from_dict(self, data: dict) -> ArtifactDTO:
        """
        Converts a dictionary from JSON deserialization to an Application ArtifactDTO.
        """
        return ArtifactDTO(
            inventory_id=UUID(data["inventory_id"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            acquisition_date=datetime.fromisoformat(data["acquisition_date"]),
            name=data["name"],
            department=data["department"],
            era=EraDTO(value=data["era"]["value"]),
            material=MaterialDTO(value=data["material"]["value"]),
            description=data.get("description"),
        )
