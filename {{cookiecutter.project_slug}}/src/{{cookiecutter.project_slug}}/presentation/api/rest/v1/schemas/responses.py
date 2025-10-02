from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO


class MaterialResponse(BaseModel):
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


class EraResponse(BaseModel):
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


class ArtifactResponse(BaseModel):
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
    era: EraResponse = Field(..., description="Historical era of the artifact")
    material: MaterialResponse = Field(..., description="Material of the artifact")
    description: str | None = Field(
        None, max_length=1000, description="Optional description of the artifact"
    )

    @field_validator("acquisition_date")
    @classmethod
    def validate_acquisition_date(cls, value: datetime) -> datetime:
        from datetime import UTC
        if value > datetime.now(UTC):
            raise ValueError("Acquisition date cannot be in the future")
        return value

    @model_validator(mode="after")
    def validate_dates(self) -> "ArtifactResponse":
        if self.acquisition_date > self.created_at:
            raise ValueError("Acquisition date cannot be later than created_at")
        return self

    @classmethod
    def from_dto(cls, dto: ArtifactDTO) -> "ArtifactResponse":
        return cls(
            inventory_id=dto.inventory_id,
            name=dto.name,
            description=dto.description,
            era=dto.era,
            material=dto.material,
            acquisition_date=dto.acquisition_date,
            department=dto.department,
        )
