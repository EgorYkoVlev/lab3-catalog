import pytest

from dataclasses import FrozenInstanceError
from mediacatalog.errors import InvalidEntityError
from mediacatalog.models import MediaItem


def test_create_media_item():
    item = MediaItem(
        id="11324",
        name="Титаник",
        category="Фильм",
        year=1997,
        duration_minutes=194,
        creator="Джеймс Кэмерон",
    )
    assert item.id == "11324"
    assert item.name == "Титаник"
    assert item.category == "Фильм"
    assert item.year == 1997
    assert item.duration_minutes == 194
    assert item.creator == "Джеймс Кэмерон"


def test_update_media_item():
    item = MediaItem(
        id="11324",
        name="Титаник",
        category="Фильм",
        year=1997,
        duration_minutes=194,
        creator="Джеймс Кэмерон",
    )
    with pytest.raises(FrozenInstanceError):
        item.name = "Британик"


def test_empty_field_id():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="",
            name="Титаник",
            category="Фильм",
            year=1997,
            duration_minutes=194,
            creator="Джеймс Кэмерон",
        )


def test_empty_field_name():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="  ",
            category="Фильм",
            year=1997,
            duration_minutes=194,
            creator="Джеймс Кэмерон",
        )


def test_invalid_field_type_category():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="Титаник",
            category=67.43,
            year=1997,
            duration_minutes=194,
            creator="Джеймс Кэмерон",
        )


def test_field_year_out_of_range():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="Титаник",
            category="Фильм",
            year=2070,
            duration_minutes=194,
            creator="Джеймс Кэмерон",
        )


def test_feld_duration_minutes_less_than_zero():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="Титаник",
            category="Фильм",
            year=2026,
            duration_minutes=-3,
            creator="Джеймс Кэмерон",
        )


def test_feld_duration_minutes_is_bool():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="Титаник",
            category="Фильм",
            year=2026,
            duration_minutes=True,
            creator="Джеймс Кэмерон",
        )


def test_invalid_field_type_creator():
    with pytest.raises(InvalidEntityError):
        MediaItem(
            id="11324",
            name="Титаник",
            category="Фильм",
            year=2026,
            duration_minutes=194,
            creator=True,
        )
