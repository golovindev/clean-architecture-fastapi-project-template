from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MaterialPydanticDTO(BaseModel):
    """Pydantic DTO for Material, used in infrastructure layer for external communication."""
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    value: Literal[
        "ceramic",
        "metal",
        "stone",
        "glass",
        "bone",
        "wood",
        "textile",
        "other",
    ]


class EraPydanticDTO(BaseModel):
    """Pydantic DTO for Era, used in infrastructure layer for external communication."""
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    value: Literal[
        "paleolithic",
        "neolithic",
        "bronze_age",
        "iron_age",
        "antiquity",
        "middle_ages",
        "modern",
    ]


class ArtifactPydanticDTO(BaseModel):
    """Pydantic DTO for Artifact, used in infrastructure layer for external communication."""
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        from_attributes=True,
        validate_default=True,
    )

    inventory_id: UUID = Field(..., description="Unique identifier of the artifact")
    created_at: datetime = Field(
        description="Timestamp when the artifact record was created (UTC)",
    )
    acquisition_date: datetime = Field(
        ..., description="Date when the artifact was acquired"
    )
    name: str = Field(
        ..., min_length=2, max_length=100, description="Name of the artifact"
    )
    department: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Department responsible for the artifact",
    )
    era: EraPydanticDTO = Field(..., description="Historical era of the artifact")
    material: MaterialPydanticDTO = Field(..., description="Material of the artifact")
    description: str | None = Field(
        None, max_length=1000, description="Optional description of the artifact"
    )


class ArtifactAdmissionNotificationPydanticDTO(BaseModel):
    """Pydantic DTO for Artifact Admission Notification, used for message broker communication."""
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    inventory_id: UUID
    name: str
    acquisition_date: datetime
    department: str


class ArtifactCatalogPublicationPydanticDTO(BaseModel):
    """Pydantic DTO for Artifact Catalog Publication, used for external catalog API communication."""
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    inventory_id: UUID
    name: str
    era: EraPydanticDTO
    material: MaterialPydanticDTO
    description: str | None = None
