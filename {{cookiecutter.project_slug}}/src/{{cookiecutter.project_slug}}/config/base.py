from typing import Literal, cast, final

from pydantic import Field, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings


@final
class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name (str): Name of the application.
        environment (Literal["local", "dev", "prod"]): Application environment.
        log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR"]): Logging level.
        debug (bool): Debug mode flag.
        postgres_user (str): PostgreSQL username.
        postgres_password (str): PostgreSQL password.
        postgres_server (str): PostgreSQL server host.
        postgres_port (int): PostgreSQL server port.
        postgres_db (str): PostgreSQL database name.
        museum_api_base (str): Base URL for the external museum API.
        catalog_api_base (str): Base URL for the public catalog API.
        external_api_base_url (str): Alias for museum_api_base.
        catalog_api_base_url (str): Alias for catalog_api_base.
        http_timeout (float): HTTP request timeout in seconds.
        broker_url (str): Message broker URL.
        broker_new_artifact_queue (str): Queue name for new artifact messages.
        publish_retries (int): Number of retries for publishing operations.
        publish_retry_backoff (float): Backoff factor for publish retries.
        redis_url (RedisDsn): Redis connection URL.
        redis_password (str): Redis password.
        redis_port (int): Redis port.
        redis_host (str): Redis host.
        redis_db (int): Redis database number.
        redis_cache_ttl (int): Time-to-live for Redis cache entries in seconds.
        redis_cache_prefix (str): Prefix for Redis cache keys.
        cors_origins (list[str]): List of allowed CORS origins.
        cors_allow_credentials (bool): Whether CORS requests should support credentials.
        cors_allow_methods (list[str]): List of allowed CORS HTTP methods.
        cors_allow_headers (list[str]): List of allowed CORS HTTP headers.
    """

    app_name: str = "Antiquarium Service"
    environment: Literal["local", "dev", "prod"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    debug: bool = Field(False, alias="DEBUG")

    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_server: str = Field(..., alias="POSTGRES_SERVER")
    postgres_port: int = Field(5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    museum_api_base: str = Field(
        "https://api.antiquarium-museum.ru", alias="MUSEUM_API_BASE"
    )
    catalog_api_base: str = Field(
        "https://catalog.antiquarium-museum.ru", alias="CATALOG_API_BASE"
    )

    # Aliases for compatibility
    external_api_base_url: str = Field(
        "https://api.antiquarium-museum.ru", alias="EXTERNAL_API_BASE_URL"
    )
    catalog_api_base_url: str = Field(
        "https://catalog.antiquarium-museum.ru", alias="CATALOG_API_BASE_URL"
    )

    http_timeout: float = Field(10.0, alias="HTTP_TIMEOUT")

    broker_url: str = Field(
        ..., alias="BROKER_URL"
    )  # e.g. amqp://guest:guest@localhost:5672/
    broker_new_artifact_queue: str = Field(
        "new_artifacts", alias="BROKER_NEW_ARTIFACT_QUEUE"
    )

    publish_retries: int = Field(3, alias="PUBLISH_RETRIES")
    publish_retry_backoff: float = Field(0.5, alias="PUBLISH_RETRY_BACKOFF")

    # Redis Configuration
    redis_url: RedisDsn = Field(
        RedisDsn("redis://:redis_password@redis:6379/0"), alias="REDIS_URL"
    )
    redis_password: str = Field("redis_password", alias="REDIS_PASSWORD")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_host: str = Field("redis", alias="REDIS_HOST")
    redis_db: int = Field(0, alias="REDIS_DB")
    redis_cache_ttl: int = Field(3600, alias="REDIS_CACHE_TTL")  # 1 hour default TTL
    redis_cache_prefix: str = Field("antiques:", alias="REDIS_CACHE_PREFIX")

    cors_origins: list[str] = Field(
        ["http://localhost:3000", "http://localhost:8080"], alias="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = Field(True, alias="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list[str] = Field(
        ["GET", "POST", "PUT", "DELETE", "OPTIONS"], alias="CORS_ALLOW_METHODS"
    )
    cors_allow_headers: list[str] = Field(["*"], alias="CORS_ALLOW_HEADERS")

    @computed_field
    def database_url(self) -> PostgresDsn:
        """
        Constructs the PostgreSQL database URL.

        Returns:
            PostgresDsn: The constructed database URL.
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_server,
            port=self.postgres_port,
            path=self.postgres_db,
        )

    @computed_field
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        """
        Returns the SQLAlchemy compatible database URI.

        Returns:
            PostgresDsn: The SQLAlchemy database URI.
        """
        return cast("PostgresDsn", self.database_url)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
