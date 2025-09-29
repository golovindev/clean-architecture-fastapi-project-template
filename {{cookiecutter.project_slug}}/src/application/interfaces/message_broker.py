from typing import Protocol

from src.application.dtos.artifact import ArtifactAdmissionNotificationDTO


class MessageBrokerPublisherProtocol(Protocol):
    async def publish_new_artifact(
        self, artifact: ArtifactAdmissionNotificationDTO
    ) -> None: ...
