from dataclasses import dataclass, field
import json
import logging
from typing import final

from faststream.kafka import KafkaBroker

from src.application.dtos.artifact import ArtifactAdmissionNotificationDTO
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class KafkaPublisher(MessageBrokerPublisherProtocol):
    broker: KafkaBroker
    topic: str = field(default="new_artifacts")

    async def publish_new_artifact(
        self, artifact: ArtifactAdmissionNotificationDTO
    ) -> None:
        try:
            await self.broker.publish(
                key=artifact.inventory_id,
                message=json.dumps(artifact.model_dump(), ensure_ascii=False),
                topic=self.topic,
            )
        except Exception as e:
            logging.error("Failed to publish artifact: %s", e)
            raise
