# -*- coding: utf-8 -*-


class EndOfStream(Exception):
    pass


class InvalidSyntaxError(Exception):
    pass


class InvalidCommandFormat(InvalidSyntaxError):
    pass


class TokenNotFound(InvalidSyntaxError):
    pass


class DeprecatedSyntax(InvalidSyntaxError):
    pass


class TokenizationFatalFailure(InvalidSyntaxError):
    pass


class RenderingError(Exception):
    pass


class ApertureSelectionError(Exception):
    pass


class FeatureNotSupportedError(Exception):
    pass


def suppress_context(exc: Exception) -> Exception:
    exc.__suppress_context__ = True
    return exc
