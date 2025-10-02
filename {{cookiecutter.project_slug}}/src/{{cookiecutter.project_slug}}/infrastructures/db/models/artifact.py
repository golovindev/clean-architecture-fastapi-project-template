from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, registry

mapper_registry = registry()


@mapper_registry.mapped
class ArtifactModel:
    __tablename__ = "artifacts"
    __table_args__ = (
        Index("ix_artifacts_name", "name"),
        Index("ix_artifacts_department", "department"),
    )

    def __init__(
            self,
            *,
            inventory_id: UUID,
            created_at: datetime,
            acquisition_date: datetime,
            name: str,
            department: str,
            era: str,
            material: str,
            description: str | None = None,
    ) -> None:
        self.inventory_id = inventory_id
        self.created_at = created_at
        self.acquisition_date = acquisition_date
        self.name = name
        self.department = department
        self.era = era
        self.material = material
        self.description = description

    inventory_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )
    acquisition_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    department: Mapped[str] = mapped_column(String(length=255), nullable=False)
    era: Mapped[str] = mapped_column(String(length=50), nullable=False)
    material: Mapped[str] = mapped_column(String(length=50), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<ArtifactModel(inventory_id={self.inventory_id!s}, "
            f"name={self.name!r}, department={self.department!r})>"
        )
