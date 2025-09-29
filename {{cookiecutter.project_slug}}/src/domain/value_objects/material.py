from dataclasses import dataclass
from typing import ClassVar, final

from src.domain.exceptions import InvalidMaterialException


@final
@dataclass(frozen=True, slots=True, kw_only=True, order=True)
class Material:
    _allowed_values: ClassVar[set[str]] = {
        "ceramic",
        "metal",
        "stone",
        "glass",
        "bone",
        "wood",
        "textile",
        "other",
    }
    value: str

    def __post_init__(self) -> None:
        if self.value not in self._allowed_values:
            raise InvalidMaterialException("Invalid material: %s", self.value)

    def __str__(self) -> str:
        return self.value
