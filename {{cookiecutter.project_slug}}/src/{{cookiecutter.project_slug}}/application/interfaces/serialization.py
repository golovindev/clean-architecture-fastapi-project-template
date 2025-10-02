from typing import Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO


class SerializationMapperProtocol(Protocol):
    """Protocol for serialization/deserialization of Application DTOs.

    This interface allows the Application layer to serialize DTOs
    without depending on Infrastructure implementations.
    """

    def to_dict(self, dto: ArtifactDTO) -> dict:
        """Convert Application DTO to dict for serialization (e.g., caching)."""
        ...

    def from_dict(self, data: dict) -> ArtifactDTO:
        """Convert dict from deserialization to Application DTO."""
        ...
