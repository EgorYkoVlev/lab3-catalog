class CatalogError(Exception):
    """Базовое исключение для всех ошибок каталога."""


class InvalidEntityError(CatalogError):
    """Сущность не прошла проверку инвариантов."""


class DuplicateIdError(CatalogError):
    """Два объекта с одним ID не могут находиться в каталоге."""


class ObjectNotFoundError(CatalogError):
    """Объект отсутствует в каталоге."""


class UnsupportedFormatVersionError(CatalogError):
    """Неизвестная версия формата отклоняется."""


class CorruptedFileError(CatalogError):
    """Повреждённый документ не должен частично изменять существующий каталог."""
