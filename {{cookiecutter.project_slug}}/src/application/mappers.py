from dataclasses import dataclass
from datetime import datetime
from typing import final
from uuid import UUID

from src.application.dtos.artifact import ArtifactDTO, EraDTO, MaterialDTO
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


@final
@dataclass(frozen=True, slots=True)
class ArtifactMapper(DtoEntityMapperProtocol):
    def to_dto(self, entity: ArtifactEntity) -> ArtifactDTO:
        return ArtifactDTO(
            inventory_id=entity.inventory_id,
            created_at=entity.created_at,
            acquisition_date=entity.acquisition_date,
            name=entity.name,
            department=entity.department,
            era=EraDTO(value=entity.era.value),
            material=MaterialDTO(value=entity.material.value),
            description=entity.description,
        )

    def to_entity(self, dto: ArtifactDTO) -> ArtifactEntity:
        return ArtifactEntity(
            inventory_id=dto.inventory_id,
            name=dto.name,
            acquisition_date=dto.acquisition_date,
            department=dto.department,
            era=Era(value=dto.era.value),
            material=Material(value=dto.material.value),
            description=dto.description,
        )

    def to_dict(self, dto: ArtifactDTO) -> dict:
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
