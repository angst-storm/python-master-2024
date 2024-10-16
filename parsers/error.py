"""Парсер, который выбрасывает "намеренную" ошибку (для целей тестирования)"""

class ParseqIntentionalException(BaseException):
    pass


def parse() -> dict[str, bytearray]:
    raise ParseqIntentionalException
