from datetime import UTC, datetime
from typing import Literal, final
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


@final
class MaterialDTO(BaseModel):
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


@final
class EraDTO(BaseModel):
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


@final
class ArtifactDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
        from_attributes=True,
        validate_default=True,
    )

    inventory_id: UUID = Field(..., description="Unique identifier of the artifact")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
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
    era: EraDTO = Field(..., description="Historical era of the artifact")
    material: MaterialDTO = Field(..., description="Material of the artifact")
    description: str | None = Field(
        None, max_length=1000, description="Optional description of the artifact"
    )

    @field_validator("acquisition_date")
    @classmethod
    def validate_acquisition_date(cls, value: datetime) -> datetime:
        if value > datetime.now(UTC):
            raise ValueError("Acquisition date cannot be in the future")
        return value

    @model_validator(mode="after")
    def validate_dates(self) -> "ArtifactDTO":
        if self.acquisition_date > self.created_at:
            raise ValueError("Acquisition date cannot be later than created_at")
        return self


@final
class ArtifactAdmissionNotificationDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    inventory_id: UUID
    name: str
    acquisition_date: datetime
    department: str


@final
class ArtifactCatalogPublicationDTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
    inventory_id: UUID
    name: str
    era: EraDTO
    material: MaterialDTO
    description: str | None = None
