import sys
from pathlib import Path

from mediacatalog.catalog import Catalog
from mediacatalog.errors import CatalogError
from mediacatalog.models import MediaItem

DEMO_FILE = Path("demo_catalog.json")


def main() -> None:
    catalog = Catalog()
    catalog.add(MediaItem("1", "Титаник", "Фильм", 1997, 194, "Джеймс Кэмерон"))
    catalog.add(MediaItem("2", "Матрица", "Фильм", 1999, 136, "Вачовски"))
    catalog.add(MediaItem("3", "Kind of Blue", "Музыка", 1959, 46, "Майлз Дэвис"))

    print(f"Элементов в каталоге: {len(catalog)}")
    for item in catalog:
        print(" ", item)

    print("Поиск по имени 'титаник':", catalog.find_by_name("титаник"))
    print("Поиск по категории 'Музыка':", catalog.find_by_category("Музыка"))

    catalog.save(DEMO_FILE)
    restored = Catalog()
    restored.load(DEMO_FILE)
    print(
        "После сохранения и загрузки данные совпали:", list(restored) == list(catalog)
    )

    try:
        catalog.get("нет такого")
    except CatalogError as exc:
        print("Ожидаемая ошибка:", exc)


if __name__ == "__main__":
    sys.exit(main())
