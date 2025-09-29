from dataclasses import dataclass
from typing import final
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.application.interfaces.repositories import ArtifactRepositoryProtocol
from src.domain.entities.artifact import ArtifactEntity
from src.infrastructures.db.exceptions import (
    RepositoryConflictError,
    RepositorySaveError,
)
from src.infrastructures.db.models.artifact import ArtifactModel


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactRepositorySQLAlchemy(ArtifactRepositoryProtocol):
    session: AsyncSession

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
            return artifact_model.to_dataclass()
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
                model.name = artifact.name
                model.era = artifact.era.value
                model.material = artifact.material.value
                model.description = artifact.description
                model.acquisition_date = artifact.acquisition_date
                model.department = artifact.department
            else:
                model = ArtifactModel.from_dataclass(artifact)

            self.session.add(model)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            raise RepositoryConflictError(
                f"Conflict while saving artifact '{artifact.inventory_id}': {e}"
            ) from e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositorySaveError(
                f"Failed to save artifact '{artifact.inventory_id}': {e}"
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise RepositorySaveError(
                f"Unexpected error while saving artifact '{artifact.inventory_id}': {e}"
            ) from e
