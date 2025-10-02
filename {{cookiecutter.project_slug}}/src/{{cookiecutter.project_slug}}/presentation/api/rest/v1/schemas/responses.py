from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


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
