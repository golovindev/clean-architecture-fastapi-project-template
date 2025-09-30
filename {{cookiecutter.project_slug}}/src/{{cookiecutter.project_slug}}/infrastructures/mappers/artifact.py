from dataclasses import dataclass
from typing import final

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from {{cookiecutter.project_slug}}.infrastructures.dtos.artifact import (
    ArtifactAdmissionNotificationPydanticDTO,
    ArtifactCatalogPublicationPydanticDTO,
    ArtifactPydanticDTO,
    EraPydanticDTO,
    MaterialPydanticDTO,
)


@final
@dataclass(frozen=True, slots=True)
class InfrastructureArtifactMapper:
    def to_pydantic_dto(self, dto: ArtifactDTO) -> ArtifactPydanticDTO:
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
        return ArtifactAdmissionNotificationPydanticDTO(
            inventory_id=dto.inventory_id,
            name=dto.name,
            acquisition_date=dto.acquisition_date,
            department=dto.department,
        )

    def to_catalog_publication_pydantic(
        self, dto: ArtifactCatalogPublicationDTO
    ) -> ArtifactCatalogPublicationPydanticDTO:
        return ArtifactCatalogPublicationPydanticDTO(
            inventory_id=dto.inventory_id,
            name=dto.name,
            era=EraPydanticDTO(value=dto.era.value),
            material=MaterialPydanticDTO(value=dto.material.value),
            description=dto.description,
        )
