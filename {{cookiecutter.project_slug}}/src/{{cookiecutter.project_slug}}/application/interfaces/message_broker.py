from typing import Protocol

from {{cookiecutter.project_slug}}.application.dtos.artifact import ArtifactAdmissionNotificationDTO


class MessageBrokerPublisherProtocol(Protocol):
    async def publish_new_artifact(
        self, artifact: ArtifactAdmissionNotificationDTO
    ) -> None: ...
