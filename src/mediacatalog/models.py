from dataclasses import dataclass
from datetime import date
from .errors import InvalidEntityError


def require_not_empty_str(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise InvalidEntityError(f"поле {field_name} должно быть непустой строкой")


@dataclass(frozen=True)
class MediaItem:
    item_id: str
    name: str
    category: str
    year: int
    duration_minutes: int
    creator: str

    def __post_init__(self) -> None:
        require_not_empty_str(self.item_id, "id")
        require_not_empty_str(self.name, "name")
        require_not_empty_str(self.category, "category")
        require_not_empty_str(self.creator, "creator")

        object.__setattr__(self, "item_id", self.item_id.strip())
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "category", self.category.strip())
        object.__setattr__(self, "creator", self.creator.strip())

        if (
            not isinstance(self.year, int)
            or self.year < 1800
            or self.year > date.today().year
        ):
            raise InvalidEntityError(
                "поле year должно быть целым числом в диапазоне [1800, текущий год]"
            )

        if (
            not isinstance(self.duration_minutes, int)
            or isinstance(self.duration_minutes, bool)
            or self.duration_minutes <= 0
        ):
            raise InvalidEntityError(
                "поле duration_minutes должно быть натуральным числом"
            )
