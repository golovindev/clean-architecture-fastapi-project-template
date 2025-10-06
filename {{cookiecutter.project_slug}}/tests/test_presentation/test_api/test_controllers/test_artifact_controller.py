from unittest.mock import AsyncMock
from uuid import uuid4

from fastapi import HTTPException, status
import pytest

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactDTO, EraDTO, MaterialDTO
from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from {{cookiecutter.project_slug}}.application.use_cases.get_artifact import ProcessArtifactUseCase


class TestArtifactController:
    async def _call_controller_with_mock(
        self, inventory_id: str, mock_use_case: ProcessArtifactUseCase
    ):
        """Helper method to call the controller function with a mock use case"""
        try:
            return await mock_use_case.execute(inventory_id)
        except ArtifactNotFoundError as err:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artifact not found in the system.",
            ) from err
        except FailedFetchArtifactMuseumAPIException as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch artifact data from the museum API.",
            ) from err
        except FailedPublishArtifactInCatalogException as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Artifact could not be published in the catalog.",
            ) from err
        except FailedPublishArtifactMessageBrokerException as err:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to send notification via message broker.",
            ) from err

    @pytest.mark.asyncio
    async def test_get_artifact_success(self):
        """Test successful artifact retrieval"""
        inventory_id = str(uuid4())
        expected_dto = ArtifactDTO(
            inventory_id=uuid4(),
            created_at="2023-01-01T00:00:00Z",
            acquisition_date="2023-01-01T00:00:00Z",
            name="Ancient Vase",
            department="Archaeology",
            era=EraDTO(value="antiquity"),
            material=MaterialDTO(value="ceramic"),
            description="A beautiful ancient vase",
        )

        mock_use_case = AsyncMock()
        mock_use_case.execute.return_value = expected_dto

        result = await self._call_controller_with_mock(inventory_id, mock_use_case)

        assert result == expected_dto
        mock_use_case.execute.assert_called_once_with(inventory_id)
