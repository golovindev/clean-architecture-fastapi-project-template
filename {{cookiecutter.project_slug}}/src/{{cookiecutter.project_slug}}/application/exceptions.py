from typing import final


@final
class ArtifactNotFoundError(Exception): ...


@final
class FailedFetchArtifactMuseumAPIException(Exception): ...


@final
class FailedPublishArtifactMessageBrokerException(Exception): ...


@final
class FailedPublishArtifactInCatalogException(Exception): ...
