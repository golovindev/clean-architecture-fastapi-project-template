from typing import Protocol

from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol


class UnitOfWorkProtocol(Protocol):
    """
    Protocol for a Unit of Work.

    This protocol defines the interface for managing transactions and
    the lifecycle of repositories within a single business transaction.
    """

    repository: ArtifactRepositoryProtocol

    async def __aenter__(self) -> "UnitOfWorkProtocol":
        """Enters the asynchronous context manager."""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exits the asynchronous context manager."""
        ...

    async def commit(self) -> None:
        """Commits the current transaction."""
        ...

    async def rollback(self) -> None:
        """Rolls back the current transaction."""
        ...
