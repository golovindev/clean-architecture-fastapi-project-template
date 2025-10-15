from polyfactory.factories import ModelFactory
from polyfactory.field_meta import PostProcessedField

from tests.faker import uuid4, word, text, date_time_this_century

from {{cookiecutter.project_slug}}.application.dtos.artifact import (
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from {{cookiecutter.project_slug}}.domain.entities.artifact import (
    ArtifactEntity,
    Material,
    Era,
)


class MaterialDTOFactory(ModelFactory[MaterialDTO]):
    """Factory for MaterialDTO objects."""

    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ])
    )


class EraDTOFactory(ModelFactory[EraDTO]):
    """Factory for EraDTO objects."""

    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "paleolithic", "neolithic", "bronze_age", "iron_age", "antiquity",
            "middle_ages", "modern"
        ])
    )


class ArtifactDTOFactory(ModelFactory[ArtifactDTO]):
    """Factory for ArtifactDTO objects."""

    inventory_id = PostProcessedField(lambda: uuid4())
    acquisition_date = PostProcessedField(lambda: date_time_this_century())
    name = PostProcessedField(lambda: word())
    department = PostProcessedField(lambda: word())
    era = ModelFactory.create_factory(EraDTOFactory)
    material = ModelFactory.create_factory(MaterialDTOFactory)
    description = PostProcessedField(lambda: text())
    created_at = PostProcessedField(lambda: date_time_this_century())


class MaterialFactory(ModelFactory[Material]):
    """Factory for Material value objects."""

    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "ceramic", "metal", "stone", "glass", "bone", "wood", "textile", "other"
        ])
    )


class EraFactory(ModelFactory[Era]):
    """Factory for Era value objects."""

    value = PostProcessedField(
        lambda: ModelFactory.__random__.choice([
            "paleolithic", "neolithic", "bronze_age", "iron_age", "antiquity",
            "middle_ages", "modern"
        ])
    )


class ArtifactEntityFactory(ModelFactory[ArtifactEntity]):
    """Factory for ArtifactEntity objects."""

    inventory_id = PostProcessedField(lambda: uuid4())
    created_at = PostProcessedField(lambda: date_time_this_century())
    acquisition_date = PostProcessedField(lambda: date_time_this_century())
    name = PostProcessedField(lambda: word())
    department = PostProcessedField(lambda: word())
    era = ModelFactory.create_factory(EraFactory)
    material = ModelFactory.create_factory(MaterialFactory)
    description = PostProcessedField(lambda: text())
