from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.use_cases.get_artifact import GetArtifactUseCase
from src.domain.entities.artifact import ArtifactEntity


class TestGetArtifactUseCase:
    @pytest.mark.asyncio
    async def test_execute_artifact_found_in_repository(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_entity: ArtifactEntity,
        sample_artifact_dto: ArtifactDTO,
    ):
        """Test successful execution when artifact is found in local repository"""
        inventory_id = str(sample_artifact_entity.inventory_id)
        mock_uow.repositories.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        result = await get_artifact_use_case.execute(inventory_id)

        assert result == sample_artifact_dto
        mock_uow.repositories.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_mapper.to_dto.assert_called_once_with(sample_artifact_entity)
        mock_uow.repositories.save.assert_not_called()
        mock_museum_api = get_artifact_use_case.museum_api_client
        mock_museum_api.fetch_artifact.assert_not_called()
