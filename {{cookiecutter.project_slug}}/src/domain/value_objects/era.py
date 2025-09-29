from dataclasses import dataclass
from typing import ClassVar, final

from src.domain.exceptions import InvalidEraException


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Era:
    _allowed_values: ClassVar[set[str]] = {
        "paleolithic",
        "neolithic",
        "bronze_age",
        "iron_age",
        "antiquity",
        "middle_ages",
        "modern",
    }
    value: str

    def __post_init__(self) -> None:
        if self.value not in self._allowed_values:
            raise InvalidEraException("Invalid era: %s", self.value)

    def __str__(self) -> str:
        return self.value
