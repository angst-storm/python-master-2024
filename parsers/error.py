class ParseqIntentionalException(BaseException):
    pass


def parse() -> dict[str, bytearray]:
    raise ParseqIntentionalException
