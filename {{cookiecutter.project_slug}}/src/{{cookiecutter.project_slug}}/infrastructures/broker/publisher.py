from dataclasses import dataclass, field
import json
from typing import final

import structlog
from faststream.kafka import KafkaBroker

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactAdmissionNotificationDTO
from {{cookiecutter.project_slug}}.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from {{cookiecutter.project_slug}}.infrastructures.dtos.artifact import (
    ArtifactAdmissionNotificationPydanticDTO,
)
from {{cookiecutter.project_slug}}.infrastructures.mappers.artifact import InfrastructureArtifactMapper


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class KafkaPublisher(MessageBrokerPublisherProtocol):
    """
    Kafka implementation of the MessageBrokerPublisherProtocol.
    Publishes artifact admission notifications to a Kafka topic.
    """

    broker: KafkaBroker
    topic: str = field(default="new_artifacts")
    mapper: InfrastructureArtifactMapper

    async def publish_new_artifact(
        self, artifact: ArtifactAdmissionNotificationDTO
    ) -> None:
        """
        Publishes a new artifact admission notification to Kafka.

        Args:
            artifact: The ArtifactAdmissionNotificationDTO to publish.

        Raises:
            Exception: If publishing the message fails.
        """
        try:
            pydantic_artifact = self.mapper.to_admission_notification_pydantic(artifact)
            await self.broker.publish(
                key=pydantic_artifact.inventory_id,
                message=json.dumps(pydantic_artifact.model_dump(), ensure_ascii=False),
                topic=self.topic,
            )
        except Exception as e:
            logger = structlog.get_logger(__name__)
            logger.error("Failed to publish artifact", error=str(e))
            raise
