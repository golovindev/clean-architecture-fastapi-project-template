from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from {{cookiecutter.project_slug}}.domain.exceptions import (
    DomainValidationError,
    InvalidEraException,
    InvalidMaterialException,
)


def setup_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ArtifactNotFoundError)
    async def artifact_not_found_exception_handler(
        request: Request,
        exc: ArtifactNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": str(exc)},
        )

    @app.exception_handler(FailedFetchArtifactMuseumAPIException)
    async def failed_fetch_artifact_museum_api_exception_handler(
        request: Request,
        exc: FailedFetchArtifactMuseumAPIException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )

    @app.exception_handler(FailedPublishArtifactInCatalogException)
    async def failed_publish_artifact_in_catalog_exception_handler(
        request: Request,
        exc: FailedPublishArtifactInCatalogException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )

    @app.exception_handler(FailedPublishArtifactMessageBrokerException)
    async def failed_publish_artifact_message_broker_exception_handler(
        request: Request,
        exc: FailedPublishArtifactMessageBrokerException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )

    @app.exception_handler(DomainValidationError)
    async def domain_validation_error_handler(
        request: Request,
        exc: DomainValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidEraException)
    async def invalid_era_exception_handler(
        request: Request,
        exc: InvalidEraException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )

    @app.exception_handler(InvalidMaterialException)
    async def invalid_material_exception_handler(
        request: Request,
        exc: InvalidMaterialException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(exc)},
        )
