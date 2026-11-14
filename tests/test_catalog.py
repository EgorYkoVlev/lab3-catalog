import pytest

from mediacatalog.catalog import Catalog
from mediacatalog.errors import (
    DuplicateIdError,
    InvalidEntityError,
    ObjectNotFoundError,
)
from mediacatalog.models import MediaItem


def make_item(**overrides) -> MediaItem:
    """Создание объекта на основе шаблона"""
    data = dict(
        item_id="1",
        name="Титаник",
        category="Фильм",
        year=1997,
        duration_minutes=194,
        creator="Джеймс Кэмерон",
    )
    data.update(overrides)
    return MediaItem(**data)


@pytest.fixture
def catalog() -> Catalog:
    """Фикстура с шаблоном каталога"""
    result = Catalog()
    result.add(make_item())
    result.add(make_item(item_id="2", name="Матрица"))
    result.add(
        make_item(
            item_id="3", name="Yellow Submarine", category="Музыка", creator="Beatles"
        )
    )
    result.add(make_item(item_id="4", year=2005))
    return result


def test_add_get_remove_item(catalog):
    """Позитивная проверка операций добавления, получения и удаления"""
    item = make_item(item_id="5", name="Крыжовник", category="Аудиокнига")

    catalog.add(item)
    assert "5" in catalog
    assert len(catalog) == 5
    assert catalog.get("5") == item

    removed_item = catalog.remove("5")
    assert removed_item == item
    assert "5" not in catalog
    assert len(catalog) == 4


def test_add_errors(catalog):
    """Негативная проверка операции добавления"""
    with pytest.raises(DuplicateIdError):
        catalog.add(make_item(item_id="2"))
    with pytest.raises(InvalidEntityError):
        catalog.add("Объект не класса MediaItem")

    assert len(catalog) == 4


def test_get_errors(catalog):
    """Негативная проверка операции получения"""
    with pytest.raises(InvalidEntityError):
        catalog.get(1)
    with pytest.raises(InvalidEntityError):
        catalog.get("")
    with pytest.raises(ObjectNotFoundError):
        catalog.get("Несуществующий ID")


def test_remove_errors(catalog):
    """Негативная проверка операции удаления"""
    with pytest.raises(InvalidEntityError):
        catalog.get(True)
    with pytest.raises(InvalidEntityError):
        catalog.get("")
    with pytest.raises(ObjectNotFoundError):
        catalog.get("Несуществующий ID")

    assert len(catalog) == 4


def test_find_by_name_is_a_copy(catalog):
    """Действия с результатами методов поиска по имени не изменяют каталог"""
    before = list(catalog)
    expected = [make_item(), make_item(item_id="4", year=2005)]
    result = catalog.find_by_name("Титаник")
    assert result == expected

    result.clear()

    assert list(catalog) == before


def test_find_by_category_is_a_copy(catalog):
    """Действия с результатами методов поиска по категории не изменяют каталог"""
    before = list(catalog)
    expected = [
        make_item(),
        make_item(item_id="2", name="Матрица"),
        make_item(item_id="4", year=2005),
    ]
    result = catalog.find_by_category("Фильм")
    assert result == expected

    result.clear()

    assert list(catalog) == before


def test_find_by_name_with_different_cases(catalog):
    """Поиск по имени нечувствителен к регистру"""
    result1 = catalog.find_by_name("Титаник")
    result2 = catalog.find_by_name("титАниК")

    assert result1 == result2


def test_find_by_name_category_errors(catalog):
    """Негативные тесты поиска по имени и категории"""
    with pytest.raises(InvalidEntityError):
        catalog.find_by_name("")
    with pytest.raises(InvalidEntityError):
        catalog.find_by_category("")
    with pytest.raises(InvalidEntityError):
        catalog.find_by_name(342)
    with pytest.raises(InvalidEntityError):
        catalog.find_by_category(False)


def test_independent_iteration_order(catalog):
    """порядок итерации документирован и детерминирован"""
    first_order = list(catalog)
    second_order = list(catalog)

    assert first_order == second_order
