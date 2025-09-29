from dataclasses import dataclass
import logging
from typing import final
from uuid import UUID

import httpx
import stamina

from src.application.dtos.artifact import (
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)
from src.application.exceptions import ArtifactNotFoundError
from src.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from src.infrastructures.dtos.artifact import (
    ArtifactCatalogPublicationPydanticDTO,
    ArtifactPydanticDTO,
)
from src.infrastructures.mappers.artifact import InfrastructureArtifactMapper

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExternalMuseumAPIClient(ExternalMuseumAPIProtocol):
    base_url: str
    client: httpx.AsyncClient
    mapper: InfrastructureArtifactMapper

    @stamina.retry(
        on=(httpx.HTTPError, httpx.RequestError),
        attempts=3,
        wait_initial=0.5,
        wait_jitter=1.0,
    )
    async def fetch_artifact(self, inventory_id: str | UUID) -> ArtifactDTO:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )
        url = f"{self.base_url}/artifacts/{inventory_id_str}"
        logger.debug("Fetching artifact from URL: %s", url)

        try:
            response = await self.client.get(url)
            if response.status_code == 404:
                logger.warning("Artifact %s not found (404).", inventory_id_str)
                raise ArtifactNotFoundError(
                    f"Artifact {inventory_id_str} not found in external service"
                )

            response.raise_for_status()
            data = response.json()

            pydantic_artifact = ArtifactPydanticDTO.model_validate(data)
            logger.debug("Successfully fetched artifact: %s", pydantic_artifact)
            
            return self.mapper.from_pydantic_dto(pydantic_artifact)

        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.exception(
                "HTTP error while fetching artifact %s: %s", inventory_id_str, e
            )
            raise
        except ValueError as e:
            logger.exception(
                "Data validation error for artifact %s : %s", inventory_id_str, e
            )
            raise
        except Exception as e:
            logger.exception(
                "Unexpected error while fetching artifact %s : %s", inventory_id_str, e
            )
            raise


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class PublicCatalogAPIClient(PublicCatalogAPIProtocol):
    base_url: str
    client: httpx.AsyncClient
    mapper: InfrastructureArtifactMapper

    @stamina.retry(
        on=(httpx.HTTPError, httpx.RequestError),
        attempts=3,
        wait_initial=1.0,
        wait_jitter=1.0,
    )
    async def publish_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> str:
        pydantic_artifact = self.mapper.to_catalog_publication_pydantic(artifact)
        
        url = f"{self.base_url}/items"
        payload = pydantic_artifact.model_dump()
        logger.debug("Publishing artifact to URL %s with payload: %s", url, payload)

        try:
            response = await self.client.post(
                url, json=payload, timeout=httpx.Timeout(10.0)
            )
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.exception("Error during HTTP request to %s: %s", url, e)
            raise
        except Exception as e:
            logger.exception("Unexpected error during publishing artifact: %s", e)
            raise Exception("Failed to publish artifact to catalog: %s", e) from e

        public_id = str(data.get("public_id", ""))
        if not public_id:
            logger.exception("Response JSON missing 'public_id' field: %s", data)
            raise ValueError("Invalid response data: missing 'public_id'")

        logger.debug("Successfully published artifact, public_id: %s", public_id)
        return public_id
