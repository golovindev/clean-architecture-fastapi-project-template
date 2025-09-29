from dataclasses import dataclass
from typing import final

from src.application.dtos.artifact import ArtifactDTO
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material


@final
@dataclass(frozen=True, slots=True)
class ArtifactMapper(DtoEntityMapperProtocol):
    def to_dto(self, entity: ArtifactEntity) -> ArtifactDTO:
        return ArtifactDTO.model_validate(entity)

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
