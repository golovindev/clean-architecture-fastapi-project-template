from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.artifact import ArtifactEntity
from src.domain.value_objects.era import Era
from src.domain.value_objects.material import Material
from tests.test_infrastructure.test_db.models.test_artifact_model import (
    TestArtifactModel,
)
from tests.test_infrastructure.test_db.repositories.test_artifact_repository_impl import (
    TestArtifactRepositorySQLAlchemy,
)


class TestArtifactRepository:
    @pytest.mark.asyncio
    async def test_save_artifact_success(self, test_session: AsyncSession):
        """Test successful artifact saving"""
        # Arrange
        repository = TestArtifactRepositorySQLAlchemy(session=test_session)
        artifact_entity = ArtifactEntity(
            inventory_id=uuid4(),
            acquisition_date=datetime(2023, 1, 1, tzinfo=UTC),
            name="Ancient Vase",
            department="Archaeology",
            era=Era(value="antiquity"),
            material=Material(value="ceramic"),
            description="A beautiful ancient vase",
        )

        await repository.save(artifact_entity)

        result = await test_session.execute(
            text(
                f"SELECT * FROM artifacts WHERE inventory_id = '{artifact_entity.inventory_id}'"
            )
        )
        db_artifact = result.fetchone()

        assert db_artifact is not None
        assert db_artifact.inventory_id == str(artifact_entity.inventory_id)
        assert db_artifact.name == artifact_entity.name
        assert db_artifact.department == artifact_entity.department
        assert db_artifact.era == artifact_entity.era.value
        assert db_artifact.material == artifact_entity.material.value
        assert db_artifact.description == artifact_entity.description
