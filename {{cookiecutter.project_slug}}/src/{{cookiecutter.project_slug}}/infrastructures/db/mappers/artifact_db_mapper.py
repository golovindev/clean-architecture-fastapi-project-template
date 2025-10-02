"""Database mapper for converting between Domain Entities and SQLAlchemy Models.

This mapper is responsible for the conversion logic between the domain layer
and the database persistence layer, following the Single Responsibility Principle.
"""

from dataclasses import dataclass
from typing import final

from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity
from {{cookiecutter.project_slug}}.domain.value_objects.era import Era
from {{cookiecutter.project_slug}}.domain.value_objects.material import Material
from {{cookiecutter.project_slug}}.infrastructures.db.models.artifact import ArtifactModel


@final
@dataclass(frozen=True, slots=True)
class ArtifactDBMapper:
    """Mapper for converting between ArtifactEntity and ArtifactModel.

    This class handles the bidirectional mapping between:
    - Domain Entities (business logic representation)
    - SQLAlchemy Models (database persistence representation)

    Benefits of separating mapper from repository:
    - Single Responsibility: Repository handles DB operations, Mapper handles conversions
    - Testability: Mapper logic can be tested independently
    - Reusability: Mapper can be used by multiple repositories if needed
    """

    def to_entity(self, model: ArtifactModel) -> ArtifactEntity:
        """Convert SQLAlchemy model to Domain Entity.

        Args:
            model: SQLAlchemy model from database.

        Returns:
            Domain entity for business logic.
        """
        return ArtifactEntity(
            inventory_id=model.inventory_id,
            created_at=model.created_at,
            acquisition_date=model.acquisition_date,
            name=model.name,
            department=model.department,
            era=Era(value=model.era),
            material=Material(value=model.material),
            description=model.description,
        )

    def to_model(self, entity: ArtifactEntity) -> ArtifactModel:
        """Convert Domain Entity to SQLAlchemy model.

        Args:
            entity: Domain entity from business logic.

        Returns:
            SQLAlchemy model for database persistence.
        """
        return ArtifactModel(
            inventory_id=entity.inventory_id,
            created_at=entity.created_at,
            acquisition_date=entity.acquisition_date,
            name=entity.name,
            department=entity.department,
            era=str(entity.era),
            material=str(entity.material),
            description=entity.description,
        )

    def update_model_from_entity(
        self, model: ArtifactModel, entity: ArtifactEntity
    ) -> None:
        """Update existing SQLAlchemy model with data from Domain Entity.

        This method is useful for update operations where you want to modify
        an existing model instance rather than creating a new one.

        Args:
            model: Existing SQLAlchemy model to update.
            entity: Domain entity with new data.
        """
        model.name = entity.name
        model.era = str(entity.era)
        model.material = str(entity.material)
        model.description = entity.description
        model.acquisition_date = entity.acquisition_date
        model.department = entity.department
