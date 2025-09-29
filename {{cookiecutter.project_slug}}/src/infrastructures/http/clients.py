from dataclasses import dataclass
import logging
from typing import final
from uuid import UUID

import httpx
import stamina

from src.application.dtos.artifact import ArtifactCatalogPublicationDTO, ArtifactDTO
from src.application.exceptions import ArtifactNotFoundError
from src.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class ExternalMuseumAPIClient(ExternalMuseumAPIProtocol):
    base_url: str
    client: httpx.AsyncClient

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

            artifact = ArtifactDTO(
                inventory_id=data["inventory_id"],
                name=data["name"],
                era=data["era"],
                material=data["material"],
                description=data["description"],
                acquisition_date=data["acquisition_date"],
                department=data["department"],
            )
            logger.debug("Successfully fetched artifact: %s", artifact)
            return artifact

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

    @stamina.retry(
        on=(httpx.HTTPError, httpx.RequestError),
        attempts=3,
        wait_initial=1.0,
        wait_jitter=1.0,
    )
    async def publish_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> str:
        url = f"{self.base_url}/items"
        payload = {
            "inventory_id": artifact.inventory_id,
            "name": artifact.name,
            "era": artifact.era,
            "material": artifact.material,
            "description": artifact.description,
        }
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
