from typing import final


@final
class InvalidMaterialException(Exception): ...


@final
class InvalidEraException(Exception): ...


@final
class DomainValidationError(Exception):
    """Raised when domain entity validation fails."""
    ...
