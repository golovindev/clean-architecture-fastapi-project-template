from typing import Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity


class DtoEntityMapperProtocol(Protocol):
    def to_dto(self, entity: ArtifactEntity) -> ArtifactDTO: ...

    def to_entity(self, dto: ArtifactDTO) -> ArtifactEntity: ...
