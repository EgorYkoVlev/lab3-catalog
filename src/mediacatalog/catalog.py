from typing import Iterator

from .models import MediaItem
from .errors import DuplicateIdError, ObjectNotFoundError, InvalidEntityError


class Catalog:
    def __init__(self) -> None:
        self._items: dict[str, MediaItem] = {}

    def add(self, item: MediaItem) -> None:
        if not isinstance(item, MediaItem):
            raise InvalidEntityError("передан объект не класса MediaItem")
        if item.item_id in self:
            raise DuplicateIdError(
                f"элемент с ID = '{item.item_id}' уже имеется в каталоге"
            )
        self._items[item.item_id] = item

    def get(self, item_id: str) -> MediaItem:
        if not isinstance(item_id, str):
            raise InvalidEntityError("поле ID - это непустая строка")

        prepared_item_id = item_id.strip()
        try:
            return self._items[prepared_item_id]
        except KeyError as err:
            raise ObjectNotFoundError(
                f"элемента с ID = '{prepared_item_id}' нет в каталоге"
            ) from err

    def remove(self, item_id: str) -> MediaItem:
        if not isinstance(item_id, str):
            raise InvalidEntityError("поле ID - это непустая строка")

        prepared_item_id = item_id.strip()
        try:
            return self._items.pop(prepared_item_id)
        except KeyError as err:
            raise ObjectNotFoundError(
                f"элемента с ID = '{prepared_item_id}' нет в каталоге"
            ) from err

    def find_by_category(self, category: str) -> list[MediaItem]:
        if not isinstance(category, str):
            raise InvalidEntityError("поле category - это непустая строка")
        prepared_category = category.strip().lower()
        return [
            item for item in self if item.category.strip().lower() == prepared_category
        ]

    def find_by_name(self, name: str) -> list[MediaItem]:
        if not isinstance(name, str):
            raise InvalidEntityError("поле name - это непустая строка")
        prepared_name = name.strip().lower()
        return [item for item in self if item.name.strip().lower() == prepared_name]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[MediaItem]:
        for item_id in sorted(self._items):
            yield self._items[item_id]

    def __contains__(self, item_id: str) -> bool:
        return item_id.strip() in self._items
