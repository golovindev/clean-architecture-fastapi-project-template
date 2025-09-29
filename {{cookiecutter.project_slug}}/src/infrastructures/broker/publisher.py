from dataclasses import dataclass, field
import json
import logging
from typing import final

from faststream.kafka import KafkaBroker

from src.application.dtos.artifact import ArtifactAdmissionNotificationDTO
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from src.infrastructures.dtos.artifact import (
    ArtifactAdmissionNotificationPydanticDTO,
)
from src.infrastructures.mappers.artifact import InfrastructureArtifactMapper


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class KafkaPublisher(MessageBrokerPublisherProtocol):
    broker: KafkaBroker
    topic: str = field(default="new_artifacts")
    mapper: InfrastructureArtifactMapper

    async def publish_new_artifact(
        self, artifact: ArtifactAdmissionNotificationDTO
    ) -> None:
        try:
            pydantic_artifact = self.mapper.to_admission_notification_pydantic(artifact)
            await self.broker.publish(
                key=pydantic_artifact.inventory_id,
                message=json.dumps(pydantic_artifact.model_dump(), ensure_ascii=False),
                topic=self.topic,
            )
        except Exception as e:
            logging.error("Failed to publish artifact: %s", e)
            raise
