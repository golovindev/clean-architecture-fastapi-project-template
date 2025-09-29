from dataclasses import dataclass
from typing import final

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repositories import ArtifactRepositoryProtocol
from src.application.interfaces.uow import UnitOfWorkProtocol
from src.infrastructures.db.repositories.artifact import ArtifactRepositorySQLAlchemy


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class UnitOfWorkSQLAlchemy(UnitOfWorkProtocol):
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
        await self.session.rollback()
