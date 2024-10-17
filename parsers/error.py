"""Парсер, который выбрасывает "намеренную" ошибку (для целей тестирования)."""

from __future__ import annotations


class ParseqIntentionalException(BaseException):
    pass


def parse() -> dict[str, bytearray]:
    """Функция парсинга."""
    raise ParseqIntentionalException
