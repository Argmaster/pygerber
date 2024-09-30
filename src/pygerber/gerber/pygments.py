"""The `pygments` module provides Pygments lexer for Gerber files."""

from __future__ import annotations

import importlib.util
import os
from typing import Any, ClassVar, Dict, List, Optional

_IS_PYGMENTS_AVAILABLE: Optional[bool] = None


def is_pygments_available() -> bool:
    """Check if the language server feature is available."""
    global _IS_PYGMENTS_AVAILABLE  # noqa: PLW0603

    if _IS_PYGMENTS_AVAILABLE is None:
        try:
            _spec_pygls = importlib.util.find_spec("pygls")
            _spec_lsprotocol = importlib.util.find_spec("lsprotocol")

        except (ImportError, ValueError):
            return False

        else:
            _IS_PYGMENTS_AVAILABLE = (_spec_pygls is not None) and (
                _spec_lsprotocol is not None
            )

    return _IS_PYGMENTS_AVAILABLE


if is_pygments_available():
    from pygments.lexer import RegexLexer
    from pygments.lexers.python import PythonLexer
    from pygments.token import Keyword, Name, Number

    class GerberLexer(RegexLexer):
        """The `GerberLexer` class is a Pygments lexer for Gerber files."""

        name = "Gerber"
        aliases: ClassVar[List[str]] = ["gerber", "gbr", "grb", "gerberx3"]
        filenames: ClassVar[List[str]] = ["*.grb", "*.gbr"]

        tokens: ClassVar[Dict[str, Any]] = {
            "root": [
                (r"X(?=[0-9]+)", Keyword),
                (r"Y(?=[0-9]+)", Keyword),
                (r"I(?=[0-9]+)", Keyword),
                (r"J(?=[0-9]+)", Keyword),
                # properties
                (r"(?<=%)FS", Keyword),
                (r"(?<=%FS)[LT][AI]", Keyword.Constant),
                (r"(?<=%)IP", Keyword),
                (r"(?<=%)IR", Keyword),
                (r"(?<=%)MO(?=MM|IN)", Keyword),
                (r"(?<=%MO)(MM|IN)", Keyword.Constant),
                (r"(?<=%)OF", Keyword),
                (r"(?<=%)AS", Keyword),
                (r"(?<=%)MI", Keyword),
                (r"(?<=%)IN", Keyword),
                (r"(?<=%)SF", Keyword),
                # attributes
                (r"(?<=%)TA", Keyword),
                (r"(?<=%)TO", Keyword),
                (r"(?<=%)TF", Keyword),
                (r"(?<=%)TD", Keyword),
                # apertures
                (r"(?<=%ADD[0-9])[._a-zA-Z$][._a-zA-Z0-9]*", Name.Class),
                (r"(?<=%ADD[0-9][0-9])[._a-zA-Z$][._a-zA-Z0-9]*", Name.Class),
                (r"(?<=%ADD[0-9][0-9][0-9])[._a-zA-Z$][._a-zA-Z0-9]*", Name.Class),
                (r"(?<=%)AD", Keyword),
                (r"(?<=%)AM", Keyword),
                (r"(?<=%AM)[._a-zA-Z$][._a-zA-Z0-9]*", Name.Class),
                (r"(?<=%)AB", Keyword),
                (r"(?<=%)SR", Keyword),
                # D codes
                (r"D0*1(?=\*)", Keyword),
                (r"D0*2(?=\*)", Keyword),
                (r"D0*3(?=\*)", Keyword),
                (r"D[0-9]+", Name.Variable),
                # G codes
                (r"G[0-9]+", Keyword),
                # M codes
                (r"M[0-9]+", Keyword),
                (r"\$[0-9]+", Name.Variable),
                (r"[+-]*[0-9]+\.[0-9]+", Number),
                (r"[+-]*[0-9]+", Number),
            ]
        }

    class PyGerberDocsLexer(PythonLexer):
        """The `PyGerberDocsLexer` class is a Pygments lexer for Gerber files."""

        name = "PyGerber Python Docs Lexer"
        aliases: ClassVar[List[str]] = ["docspygerberlexer"]
        filenames: ClassVar[List[str]] = []

        EXTRA_SYMBOLS: ClassVar[dict[str, Any]] = {
            **{  # noqa: PIE800
                "GerberX3Builder": Name.Class,
                "new_pad": Name.Function,
                "add_pad": Name.Function,
                "add_cutout_pad": Name.Function,
                "add_trace": Name.Function,
                "get_code": Name.Function,
                "set_standard_attributes": Name.Function,
            },
            **{  # noqa: PIE800
                "GerberX3Builder": Name.Class,
                "dump": Name.Function,
                "dumps": Name.Function,
                "raw": Name.Property,
            },
            **{  # noqa: PIE800
                "PadCreator": Name.Class,
                "circle": Name.Function,
                "rectangle": Name.Function,
                "rounded_rectangle": Name.Function,
                "regular_polygon": Name.Function,
                "custom": Name.Function,
            },
            **{  # noqa: PIE800
                "Pad": Name.Class,
                "set_aperture_function": Name.Function,
                "set_drill_tolerance": Name.Function,
                "set_custom_attribute": Name.Function,
            },
            **{  # noqa: PIE800
                "CustomPadCreator": Name.Class,
                "create": Name.Function,
                "add_circle": Name.Function,
                "cut_circle": Name.Function,
                "add_vector_line": Name.Function,
                "cut_vector_line": Name.Function,
                "add_center_line": Name.Function,
                "cut_center_line": Name.Function,
                "add_outline": Name.Function,
                "cut_outline": Name.Function,
                "add_polygon": Name.Function,
                "cut_polygon": Name.Function,
                "add_thermal": Name.Function,
            },
            **{  # noqa: PIE800
                "Draw": Name.Class,
            },
            **{  # noqa: PIE800
                "PadDraw": Name.Class,
            },
            **{  # noqa: PIE800
                "TraceDraw": Name.Class,
            },
        }

        def get_tokens_unprocessed(self, text: Any) -> Any:
            """Get tokens from the text."""
            if os.environ["MKDOCS_MODE"] == "1":
                for index, token, value in super().get_tokens_unprocessed(text):
                    if token is Name and value in self.EXTRA_SYMBOLS:
                        yield index, self.EXTRA_SYMBOLS[value], value
                    else:
                        yield index, token, value
            else:
                yield from super().get_tokens_unprocessed(text)
