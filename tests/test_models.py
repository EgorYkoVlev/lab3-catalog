import pytest

from dataclasses import FrozenInstanceError
from mediacatalog.errors import InvalidEntityError
from mediacatalog.models import MediaItem


def make_item(**overrides) -> MediaItem:
    """Создание объекта на основе шаблона"""
    data = dict(
        item_id="11324",
        name="Титаник",
        category="Фильм",
        year=1997,
        duration_minutes=194,
        creator="Джеймс Кэмерон",
    )
    data.update(overrides)
    return MediaItem(**data)


def test_create_media_item():
    item = make_item()

    assert item.item_id == "11324"
    assert item.name == "Титаник"
    assert item.category == "Фильм"
    assert item.year == 1997
    assert item.duration_minutes == 194
    assert item.creator == "Джеймс Кэмерон"


def test_update_media_item():
    item = make_item()

    with pytest.raises(FrozenInstanceError):
        item.name = "Британик"


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("item_id", ""),
        ("name", " "),
        ("category", 67.43),
        ("year", 2070),
        ("duration_minutes", -3),
        ("duration_minutes", True),
        ("creator", True),
    ],
)
def test_invalid_fields_rejected(field, bad_value):
    with pytest.raises(InvalidEntityError):
        make_item(**{field: bad_value})
