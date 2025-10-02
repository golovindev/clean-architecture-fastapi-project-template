import logging
from dataclasses import dataclass
from typing import final

from sqlalchemy.ext.asyncio import AsyncSession

from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UnitOfWorkSQLAlchemy(UnitOfWorkProtocol):
    """SQLAlchemy implementation of Unit of Work pattern.

    This class coordinates database transactions and provides access to repositories.
    Uses Protocol types instead of concrete implementations for better testability
    and adherence to Dependency Inversion Principle.
    """

    session: AsyncSession
    repository: ArtifactRepositoryProtocol

    async def __aenter__(self) -> "UnitOfWorkSQLAlchemy":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        logger.debug("Rolling back transaction")
        await self.session.rollback()
