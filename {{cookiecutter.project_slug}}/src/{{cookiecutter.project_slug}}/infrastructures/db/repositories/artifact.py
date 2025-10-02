from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity
from {{cookiecutter.project_slug}}.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositorySaveError,
)
from {{cookiecutter.project_slug}}.infrastructures.db.mappers.artifact_db_mapper import ArtifactDBMapper
from {{cookiecutter.project_slug}}.infrastructures.db.models.artifact import ArtifactModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactRepositorySQLAlchemy(ArtifactRepositoryProtocol):
    """SQLAlchemy implementation of the Artifact Repository.

    This repository is responsible for database operations (CRUD) only.
    Mapping logic is delegated to ArtifactDBMapper following SRP.
    """

    session: AsyncSession
    mapper: ArtifactDBMapper

    async def get_by_inventory_id(
        self, inventory_id: str | UUID
    ) -> ArtifactEntity | None:
        """Retrieve an artifact by its inventory ID.

        Args:
            inventory_id: Unique identifier of the artifact.

        Returns:
            Domain entity if found, None otherwise.

        Raises:
            RepositorySaveError: If database operation fails.
        """
        try:
            stmt = select(ArtifactModel).where(
                ArtifactModel.inventory_id == inventory_id
            )
            result = await self.session.execute(stmt)
            artifact_model = result.scalar_one_or_none()
            if artifact_model is None:
                return None
            return self.mapper.to_entity(artifact_model)
        except SQLAlchemyError as e:
            raise RepositorySaveError(
                f"Failed to retrieve artifact by inventory_id '{inventory_id}': {e}"
            ) from e

    async def save(self, artifact: ArtifactEntity) -> None:
        """Save or update an artifact in the database.

        Args:
            artifact: Domain entity to persist.

        Raises:
            RepositoryConflictError: If there's a constraint violation.
            RepositorySaveError: If database operation fails.
        """
        try:
            stmt = select(ArtifactModel).where(
                ArtifactModel.inventory_id == artifact.inventory_id
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()

            if model:
                # Update existing model using mapper
                self.mapper.update_model_from_entity(model, artifact)
            else:
                # Create new model using mapper
                model = self.mapper.to_model(artifact)

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
