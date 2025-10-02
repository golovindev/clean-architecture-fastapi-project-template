from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity
from {{cookiecutter.project_slug}}.domain.value_objects.era import Era
from {{cookiecutter.project_slug}}.domain.value_objects.material import Material
from {{cookiecutter.project_slug}}.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositorySaveError,
)
from {{cookiecutter.project_slug}}.infrastructures.db.models.artifact import ArtifactModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactRepositorySQLAlchemy(ArtifactRepositoryProtocol):
    session: AsyncSession

    def _model_to_entity(self, model: ArtifactModel) -> ArtifactEntity:
        """Convert database model to domain entity."""
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

    def _entity_to_model(self, entity: ArtifactEntity) -> ArtifactModel:
        """Convert domain entity to database model."""
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

    async def get_by_inventory_id(
        self, inventory_id: str | UUID
    ) -> ArtifactEntity | None:
        try:
            stmt = select(ArtifactModel).where(
                ArtifactModel.inventory_id == inventory_id
            )
            result = await self.session.execute(stmt)
            artifact_model = result.scalar_one_or_none()
            if artifact_model is None:
                return None
            return self._model_to_entity(artifact_model)
        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to retrieve artifact by inventory_id '{inventory_id}': {e}"
            ) from e

    async def save(self, artifact: ArtifactEntity) -> None:
        try:
            stmt = select(ArtifactModel).where(
                ArtifactModel.inventory_id == artifact.inventory_id
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Update existing model
                model.name = artifact.name
                model.era = str(artifact.era)
                model.material = str(artifact.material)
                model.description = artifact.description
                model.acquisition_date = artifact.acquisition_date
                model.department = artifact.department
            else:
                # Create new model using private converter method
                model = self._entity_to_model(artifact)

            self.session.add(model)
        except IntegrityError as e:
            raise RepositoryConflictError(
                f"Conflict while saving artifact '{artifact.inventory_id}': {e}"
            ) from e
        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to save artifact '{artifact.inventory_id}': {e}"
            ) from e
        except Exception as e:
            raise RepositorySaveError(
                f"Unexpected error while saving artifact '{artifact.inventory_id}': {e}"
            ) from e
