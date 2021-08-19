# -*- coding: utf-8 -*-


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

class RenderingError(Exception):
    pass


class ApertureSelectionError(Exception):
    pass

class NoCorespondingApertureClass(Exception):
    pass


def suppress_context(exc: Exception) -> Exception:
    exc.__suppress_context__ = True
    return exc
