import json
import os
from collections.abc import Iterable
from dataclasses import asdict, fields
from pathlib import Path

from .errors import (
    CorruptedFileError,
    DuplicateIdError,
    InvalidEntityError,
    UnsupportedFormatVersionError,
)
from .models import MediaItem

FORMAT_VERSION = 1


def save_catalog(items: Iterable[MediaItem], path: str | Path) -> None:
    path = Path(path)
    document = {
        "format_version": FORMAT_VERSION,
        "items": [asdict(item) for item in items],
    }
    tmp_path = path.with_name(path.name + ".tmp")

    try:
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(document, file, ensure_ascii=False, indent=4)
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def load_catalog(path: str | Path) -> list[MediaItem]:
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            document = json.load(file)
    except ValueError as exc:
        raise CorruptedFileError(f"JSON-файл {path} не корректен") from exc

    if not isinstance(document, dict):
        raise CorruptedFileError("корень документа должен быть JSON-объектом")

    if "format_version" not in document:
        raise CorruptedFileError("в документе нет поля format_version")

    version = document["format_version"]
    if type(version) is not int or version != FORMAT_VERSION:
        raise UnsupportedFormatVersionError(
            f"версия формата {version} не поддерживается. Поддерживаемая версия: {FORMAT_VERSION}"
        )

    raw_items = document.get("items")
    if not isinstance(raw_items, list):
        raise CorruptedFileError("поле items должно быть списком")

    required_fields = {f.name for f in fields(MediaItem)}
    items: list[MediaItem] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(raw_items):
        if not isinstance(entry, dict) or set(entry) != required_fields:
            raise CorruptedFileError(
                f"запись №{index}: объект не может быть преобразован в словарь или имеет неверный набор полей"
            )
        try:
            item = MediaItem(**entry)
        except InvalidEntityError as exc:
            raise CorruptedFileError(f"запись №{index}: {exc}") from exc
        if item.item_id in seen_ids:
            raise DuplicateIdError(f"запись №{index}: дубликат ID '{item.item_id}'")
        seen_ids.add(item.item_id)
        items.append(item)

    return items
