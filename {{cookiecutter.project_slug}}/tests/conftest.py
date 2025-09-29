from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from dishka import AsyncContainer, make_async_container
from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from src.application.interfaces.cache import CacheProtocol
from src.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from src.application.interfaces.repositories import ArtifactRepositoryProtocol
from src.application.use_cases.get_artifact import GetArtifactUseCase
from src.config.ioc.di import get_providers
from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material
from src.main import create_app
from tests.test_infrastructure.test_db.models.test_artifact_model import (
    test_mapper_registry,
)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def test_engine() -> AsyncGenerator[Any, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine: Any) -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(test_mapper_registry.metadata.create_all)

    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def test_container() -> AsyncContainer:
    return make_async_container(*get_providers())


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture
def sample_artifact_dto() -> ArtifactDTO:
    return ArtifactDTO(
        inventory_id=uuid4(),
        created_at=datetime.now(UTC),
        acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
        name="Ancient Vase",
        department="Archaeology",
        era=EraDTO(value="antiquity"),
        material=MaterialDTO(value="ceramic"),
        description="A beautiful ancient vase",
    )


@pytest.fixture
def sample_artifact_entity() -> ArtifactEntity:
    return ArtifactEntity(
        inventory_id=uuid4(),
        acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
        name="Ancient Vase",
        department="Archaeology",
        era=Era(value="antiquity"),
        material=Material(value="ceramic"),
        description="A beautiful ancient vase",
    )


@pytest.fixture
def mock_repository() -> AsyncMock:
    mock = AsyncMock(spec=ArtifactRepositoryProtocol)
    return mock


@pytest.fixture
def mock_museum_api() -> AsyncMock:
    mock = AsyncMock(spec=ExternalMuseumAPIProtocol)
    return mock


@pytest.fixture
def mock_catalog_api() -> AsyncMock:
    mock = AsyncMock(spec=PublicCatalogAPIProtocol)
    return mock


@pytest.fixture
def mock_message_broker() -> AsyncMock:
    mock = AsyncMock(spec=MessageBrokerPublisherProtocol)
    return mock


@pytest.fixture
def mock_mapper() -> MagicMock:
    mock = MagicMock(spec=DtoEntityMapperProtocol)
    return mock


@pytest.fixture
def mock_cache_client() -> AsyncMock:
    mock = AsyncMock(spec=CacheProtocol)
    # By default, return None to simulate cache miss
    mock.get.return_value = None
    return mock


@pytest.fixture
def get_artifact_use_case(
    mock_repository: AsyncMock,
    mock_museum_api: AsyncMock,
    mock_catalog_api: AsyncMock,
    mock_message_broker: AsyncMock,
    mock_mapper: MagicMock,
    mock_cache_client: AsyncMock,
) -> GetArtifactUseCase:
    return GetArtifactUseCase(
        repository=mock_repository,
        museum_api_client=mock_museum_api,
        catalog_api_client=mock_catalog_api,
        message_broker=mock_message_broker,
        artifact_mapper=mock_mapper,
        cache_client=mock_cache_client,
    )


@pytest.fixture
def sample_notification_dto() -> ArtifactAdmissionNotificationDTO:
    return ArtifactAdmissionNotificationDTO(
        inventory_id=uuid4(),
        name="Ancient Vase",
        acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
        department="Archaeology",
    )


@pytest.fixture
def sample_publication_dto() -> ArtifactCatalogPublicationDTO:
    return ArtifactCatalogPublicationDTO(
        inventory_id=uuid4(),
        name="Ancient Vase",
        era=EraDTO(value="antiquity"),
        material=MaterialDTO(value="ceramic"),
        description="A beautiful ancient vase",
    )
