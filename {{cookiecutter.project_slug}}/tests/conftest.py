from collections.abc import AsyncGenerator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock

from dishka import AsyncContainer, make_async_container
from fastapi.testclient import TestClient
from polyfactory.factories import ModelFactory
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from {{cookiecutter.project_slug}}.application.interfaces.cache import CacheProtocol
from {{cookiecutter.project_slug}}.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from {{cookiecutter.project_slug}}.application.interfaces.mappers import DtoEntityMapperProtocol
from {{cookiecutter.project_slug}}.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from {{cookiecutter.project_slug}}.application.interfaces.repositories import ArtifactRepositoryProtocol
from {{cookiecutter.project_slug}}.application.interfaces.uow import UnitOfWorkProtocol
from {{cookiecutter.project_slug}}.application.use_cases.get_artifact import GetArtifactUseCase
from {{cookiecutter.project_slug}}.config.ioc.di import get_providers
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity, Material, Era
from {{cookiecutter.project_slug}}.main import create_app
from tests.test_infrastructure.test_db.models.test_artifact_model import (
    test_mapper_registry,
)


_faker = Faker()


class MaterialDTOFactory(ModelFactory[MaterialDTO]):
    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ])
    )


class EraDTOFactory(ModelFactory[EraDTO]):
    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "paleolithic", "neolithic", "bronze_age", "iron_age", "antiquity",
            "middle_ages", "modern"
        ])
    )


class ArtifactDTOFactory(ModelFactory[ArtifactDTO]):
    inventory_id = PostProcessedField(lambda: _faker.uuid4())
    acquisition_date = PostProcessedField(lambda: _faker.date_time_this_century(tzinfo=UTC))
    name = PostProcessedField(lambda: _faker.word())
    department = PostProcessedField(lambda: _faker.word())
    era = ModelFactory.create_factory(EraDTOFactory)
    material = ModelFactory.create_factory(MaterialDTOFactory)
    description = PostProcessedField(lambda: _faker.text())
    created_at = PostProcessedField(lambda: _faker.date_time_this_century(tzinfo=UTC))


class MaterialFactory(ModelFactory[Material]):
    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ])
    )


class EraFactory(ModelFactory[Era]):
    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "paleolithic", "neolithic", "bronze_age", "iron_age", "antiquity",
            "middle_ages", "modern"
        ])
    )


class ArtifactEntityFactory(ModelFactory[ArtifactEntity]):
    inventory_id = PostProcessedField(lambda: _faker.uuid4())
    created_at = PostProcessedField(lambda: _faker.date_time_this_century(tzinfo=UTC))
    acquisition_date = PostProcessedField(lambda: _faker.date_time_this_century(tzinfo=UTC))
    name = PostProcessedField(lambda: _faker.word())
    department = PostProcessedField(lambda: _faker.word())
    era = ModelFactory.create_factory(EraFactory)
    material = ModelFactory.create_factory(MaterialFactory)
    description = PostProcessedField(lambda: _faker.text())


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
    return ArtifactDTOFactory.build()


@pytest.fixture
def sample_artifact_entity() -> ArtifactEntity:
    return ArtifactEntityFactory.build()


@pytest.fixture
def mock_repository() -> AsyncMock:
    mock = AsyncMock(spec=ArtifactRepositoryProtocol)
    return mock


@pytest.fixture
def mock_uow() -> AsyncMock:
    mock = AsyncMock(spec=UnitOfWorkProtocol)
    mock.repositories = mock_repository()
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
def mock_mapper(
    sample_notification_dto: ArtifactAdmissionNotificationDTO,
    sample_publication_dto: ArtifactCatalogPublicationDTO,
) -> MagicMock:
    mock = MagicMock(spec=DtoEntityMapperProtocol)
    # Configure default return values for new methods
    mock.to_notification_dto.return_value = sample_notification_dto
    mock.to_publication_dto.return_value = sample_publication_dto
    mock.to_dict.return_value = {}
    return mock


@pytest.fixture
def mock_cache_client() -> AsyncMock:
    mock = AsyncMock(spec=CacheProtocol)
    # By default, return None to simulate cache miss
    mock.get.return_value = None
    return mock


@pytest.fixture
def get_artifact_use_case(
    mock_uow: AsyncMock,
    mock_museum_api: AsyncMock,
    mock_catalog_api: AsyncMock,
    mock_message_broker: AsyncMock,
    mock_mapper: MagicMock,
    mock_cache_client: AsyncMock,
) -> GetArtifactUseCase:
    return GetArtifactUseCase(
        uow=mock_uow,
        museum_api_client=mock_museum_api,
        catalog_api_client=mock_catalog_api,
        message_broker=mock_message_broker,
        artifact_mapper=mock_mapper,
        cache_client=mock_cache_client,
    )


@pytest.fixture
def sample_notification_dto() -> ArtifactAdmissionNotificationDTO:
    return ArtifactAdmissionNotificationDTO(
        inventory_id=_faker.uuid4(),
        name=_faker.word(),
        acquisition_date=_faker.date_time_this_century(tzinfo=UTC),
        department=_faker.word(),
    )


@pytest.fixture
def sample_publication_dto() -> ArtifactCatalogPublicationDTO:
    return ArtifactCatalogPublicationDTO(
        inventory_id=_faker.uuid4(),
        name=_faker.word(),
        era=EraDTOFactory.build(),
        material=MaterialDTOFactory.build(),
        description=_faker.text(),
    )
