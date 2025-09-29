from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from faststream.kafka import KafkaBroker
from httpx import AsyncClient
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from src.application.mappers import ArtifactMapper
from src.application.use_cases.get_artifact import GetArtifactUseCase
from src.config.base import Settings
from src.infrastructures.broker.publisher import KafkaPublisher
from src.infrastructures.cache.redis_client import RedisCacheClient
from src.infrastructures.db.repositories.artifact import ArtifactRepositorySQLAlchemy
from src.infrastructures.db.session import create_engine, get_session_factory
from src.infrastructures.db.uow import UnitOfWorkSQLAlchemy
from src.infrastructures.http.clients import (
    ExternalMuseumAPIClient,
    PublicCatalogAPIClient,
)


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_session_factory(
        self, settings: Settings
    ) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
        engine = create_engine(str(settings.database_url), is_echo=settings.debug)
        session_factory = get_session_factory(engine)
        try:
            yield session_factory
        finally:
            await engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with factory() as session:
            yield session


class HTTPClientProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_http_client(self, settings: Settings) -> AsyncIterator[AsyncClient]:
        client = AsyncClient(timeout=settings.http_timeout)
        try:
            yield client
        finally:
            await client.aclose()


class BrokerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_broker(self, settings: Settings) -> AsyncIterator[KafkaBroker]:
        broker = KafkaBroker(settings.broker_url)
        try:
            yield broker
        finally:
            await broker.close()


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_artifact_repository(
        self, session: AsyncSession
    ) -> ArtifactRepositorySQLAlchemy:
        return ArtifactRepositorySQLAlchemy(session=session)


class UnitOfWorkProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_unit_of_work(
        self,
        session: AsyncSession,
        repository: ArtifactRepositorySQLAlchemy,
    ) -> UnitOfWorkSQLAlchemy:
        return UnitOfWorkSQLAlchemy(session=session, repository=repository)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_external_museum_api_client(
        self,
        client: AsyncClient,
        settings: Settings,
    ) -> ExternalMuseumAPIClient:
        return ExternalMuseumAPIClient(
            base_url=settings.external_api_base_url, client=client
        )

    @provide(scope=Scope.REQUEST)
    def get_public_catalog_api_client(
        self, client: AsyncClient, settings: Settings
    ) -> PublicCatalogAPIClient:
        return PublicCatalogAPIClient(
            base_url=settings.catalog_api_base_url, client=client
        )

    @provide(scope=Scope.REQUEST)
    def get_message_broker(self, broker: KafkaBroker) -> KafkaPublisher:
        return KafkaPublisher(broker=broker)


class MapperProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_artifact_mapper(self) -> ArtifactMapper:
        return ArtifactMapper()


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_cache_service(
        self, settings: Settings
    ) -> AsyncIterator[RedisCacheClient]:
        redis_client = await redis.from_url(
            str(settings.redis_url),
            encoding="utf-8",
            decode_responses=False,
            health_check_interval=30,
            max_connections=10,
            retry_on_timeout=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        cache_service = RedisCacheClient(
            client=redis_client, ttl=settings.redis_cache_ttl
        )
        try:
            yield cache_service
        finally:
            await cache_service.close()


class UseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_register_artifact_use_case(
        self,
        uow: UnitOfWorkSQLAlchemy,
        museum_api_client: ExternalMuseumAPIClient,
        catalog_api_client: PublicCatalogAPIClient,
        message_broker: KafkaPublisher,
        artifact_mapper: ArtifactMapper,
        cache_client: RedisCacheClient,
    ) -> GetArtifactUseCase:
        return GetArtifactUseCase(
            uow=uow,
            museum_api_client=museum_api_client,
            catalog_api_client=catalog_api_client,
            message_broker=message_broker,
            artifact_mapper=artifact_mapper,
            cache_client=cache_client,
        )
