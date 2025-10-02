from unittest.mock import AsyncMock, MagicMock

import pytest

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
)
from {{cookiecutter.project_slug}}.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from {{cookiecutter.project_slug}}.application.use_cases.get_artifact import GetArtifactUseCase
from {{cookiecutter.project_slug}}.domain.entities.artifact import ArtifactEntity


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
        mock_uow.repository.get_by_inventory_id.return_value = sample_artifact_entity
        mock_mapper.to_dto.return_value = sample_artifact_dto

        result = await get_artifact_use_case.execute(inventory_id)

        assert result == sample_artifact_dto
        mock_uow.repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_mapper.to_dto.assert_called_once_with(sample_artifact_entity)
        mock_uow.repository.save.assert_not_called()
        mock_museum_api = get_artifact_use_case.museum_api_client
        mock_museum_api.fetch_artifact.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_artifact_fetched_from_external_api(
        self,
        get_artifact_use_case: GetArtifactUseCase,
        mock_uow: AsyncMock,
        mock_mapper: MagicMock,
        sample_artifact_entity: ArtifactEntity,
        sample_artifact_dto: ArtifactDTO,
        sample_notification_dto: ArtifactAdmissionNotificationDTO,
        sample_publication_dto: ArtifactCatalogPublicationDTO,
    ):
        """Test successful execution when artifact is fetched from external API"""
        inventory_id = str(sample_artifact_entity.inventory_id)
        
        # Simulate artifact not found in local repository
        mock_uow.repository.get_by_inventory_id.return_value = None
        
        # Simulate successful fetch from external API
        mock_museum_api = get_artifact_use_case.museum_api_client
        mock_museum_api.fetch_artifact.return_value = sample_artifact_dto
        
        # Configure mapper
        mock_mapper.to_entity.return_value = sample_artifact_entity
        mock_mapper.to_notification_dto.return_value = sample_notification_dto
        mock_mapper.to_publication_dto.return_value = sample_publication_dto
        mock_mapper.to_dict.return_value = {"test": "data"}
        
        # Configure catalog API
        mock_catalog_api = get_artifact_use_case.catalog_api_client
        mock_catalog_api.publish_artifact.return_value = "public-123"

        result = await get_artifact_use_case.execute(inventory_id)

        # Assertions
        assert result == sample_artifact_dto
        mock_uow.repository.get_by_inventory_id.assert_called_once_with(inventory_id)
        mock_museum_api.fetch_artifact.assert_called_once()
        mock_mapper.to_entity.assert_called_once_with(sample_artifact_dto)
        mock_uow.repository.save.assert_called_once_with(sample_artifact_entity)
        
        # Verify mapper methods were called correctly
        mock_mapper.to_notification_dto.assert_called_once_with(sample_artifact_entity)
        mock_mapper.to_publication_dto.assert_called_once_with(sample_artifact_entity)
        
        # Verify external services were called
        mock_message_broker = get_artifact_use_case.message_broker
        mock_message_broker.publish_new_artifact.assert_called_once_with(
            sample_notification_dto
        )
        mock_catalog_api.publish_artifact.assert_called_once_with(
            sample_publication_dto
        )
