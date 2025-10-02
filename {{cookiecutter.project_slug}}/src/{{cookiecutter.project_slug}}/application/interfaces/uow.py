from typing import Protocol

from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol


class UnitOfWorkProtocol(Protocol):
    repository: ArtifactRepositoryProtocol

    async def __aenter__(self) -> "UnitOfWorkProtocol": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
