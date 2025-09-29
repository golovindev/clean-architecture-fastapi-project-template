from typing import Protocol

from src.application.dtos.artifact import ArtifactDTO
from src.domain.entities.artifact import ArtifactEntity


class DtoEntityMapperProtocol(Protocol):
    def to_dto(self, entity: ArtifactEntity) -> ArtifactDTO: ...

    def to_entity(self, dto: ArtifactDTO) -> ArtifactEntity: ...
