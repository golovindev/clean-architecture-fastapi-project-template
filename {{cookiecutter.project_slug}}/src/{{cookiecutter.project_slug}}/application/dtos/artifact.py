from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal, final
from uuid import UUID


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class MaterialDTO:
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
@dataclass(frozen=True, slots=True, kw_only=True)
class EraDTO:
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
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactDTO:
    inventory_id: UUID
    acquisition_date: datetime
    name: str
    department: str
    era: EraDTO
    material: MaterialDTO
    description: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if self.acquisition_date > datetime.now(UTC):
            raise ValueError("Acquisition date cannot be in the future")
        if self.acquisition_date > self.created_at:
            raise ValueError("Acquisition date cannot be later than created_at")
        if len(self.name) < 2 or len(self.name) > 100:
            raise ValueError("Name must be between 2 and 100 characters")
        if len(self.department) < 2 or len(self.department) > 100:
            raise ValueError("Department must be between 2 and 100 characters")
        if self.description is not None and len(self.description) > 1000:
            raise ValueError("Description must be at most 1000 characters")


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactAdmissionNotificationDTO:
    inventory_id: UUID
    name: str
    acquisition_date: datetime
    department: str


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactCatalogPublicationDTO:
    inventory_id: UUID
    name: str
    era: EraDTO
    material: MaterialDTO
    description: str | None = None
