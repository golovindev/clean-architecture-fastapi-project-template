import logging
from dataclasses import dataclass
from typing import final
from sqlalchemy.ext.asyncio import AsyncSession

from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol
from {{cookiecutter.project_slug}}.infrastructures.db.repositories.artifact import ArtifactRepositorySQLAlchemy

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UnitOfWorkSQLAlchemy(UnitOfWorkProtocol):
    session: AsyncSession
    repository: ArtifactRepositorySQLAlchemy

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
