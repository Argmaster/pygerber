class InvalidSyntaxError(Exception):
    pass


class InvalidCommandFormat(InvalidSyntaxError):
    pass


class TokenNotFound(InvalidSyntaxError):
    pass


class DeprecatedSyntax(InvalidSyntaxError):
    pass


class EndOfStream(InvalidSyntaxError):
    pass


def suppress_context(exc: Exception) -> Exception:
    exc.__suppress_context__ = True
    return exc
