"""Module `variable_name.py` contains a class `VariableName` used to wrap variable
name.
"""


from __future__ import annotations

from pygerber.gerberx3.parser2.macro2.expressions2.expression2 import Expression2


class VariableName2(Expression2):
    """Class wrapping variable name in macro definition."""

    name: str
