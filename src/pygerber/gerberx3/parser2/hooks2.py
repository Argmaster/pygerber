"""Parser hooks, for Gerber AST parser, version 2."""
from __future__ import annotations

from pygerber.gerberx3.parser2.context2 import Parser2Context
from pygerber.gerberx3.parser2.errors2 import Parser2Error


class Hooks2:
    """Collection of overridable hooks for Gerber AST parser, version 2."""

    def pre_parser_init(self) -> None:
        """Execute before parser initialization."""

    def post_parser_init(self) -> None:
        """Execute after parser initialization."""

    def pre_parse(self, context: Parser2Context) -> None:
        """Execute before parsing starts."""

    def post_parse(self, context: Parser2Context) -> None:
        """Execute after parsing starts."""

    def pre_parser_visit_token(self, context: Parser2Context) -> None:
        """Execute before parser visits token."""

    def post_parser_visit_token(self, context: Parser2Context) -> None:
        """Execute after parser visits token."""

    def pre_parser_visit_load_name(self, context: Parser2Context) -> None:
        """Execute before parser visits Load Name (LN) token."""

    def post_parser_visit_load_name(self, context: Parser2Context) -> None:
        """Execute after parser visits Load Name (LN) token."""

    def pre_parser_visit_add_aperture_attribute(self, context: Parser2Context) -> None:
        """Execute before parser visits Add Aperture Attribute (TA) token."""

    def post_parser_visit_add_aperture_attribute(self, context: Parser2Context) -> None:
        """Execute after parser visits Add Aperture Attribute (TA) token."""

    def pre_parser_visit_delete_attribute(self, context: Parser2Context) -> None:
        """Execute before parser visits Delete Attribute (TD) token."""

    def post_parser_visit_delete_attribute(self, context: Parser2Context) -> None:
        """Execute after parser visits Delete Attribute (TD) token."""

    def pre_parser_visit_add_file_attribute(self, context: Parser2Context) -> None:
        """Execute before parser visits Add File Attribute (TF) token."""

    def post_parser_visit_add_file_attribute(self, context: Parser2Context) -> None:
        """Execute after parser visits Add File Attribute (TF) token."""

    def pre_parser_visit_add_object_attribute(self, context: Parser2Context) -> None:
        """Execute before parser visits Add Object Attribute (TO) token."""

    def post_parser_visit_add_object_attribute(self, context: Parser2Context) -> None:
        """Execute after parser visits Add Object Attribute (TO) token."""

    def on_parser_error(self, context: Parser2Context, error: Parser2Error) -> None:
        """Execute when parsing error is thrown."""

    def on_other_error(self, context: Parser2Context, error: Exception) -> None:
        """Execute when parsing error is thrown."""
