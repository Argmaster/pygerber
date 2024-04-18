"""Tools for displaying warnings."""

from __future__ import annotations

import logging


def warn_deprecated_code(code: str, spec_section: str) -> None:
    """Display warning about deprecated code."""
    logging.warning(
        "Detected deprecated code: %s. "
        "See section %s of The Gerber Layer Format Specification Revision "
        "2023.03 - https://argmaster.github.io/pygerber/latest/gerber_specification/revision_2023_03.html",
        code,
        spec_section,
    )
