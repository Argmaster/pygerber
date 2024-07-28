"""`pygerber.nodes.d_codes.TO` module contains definition of `TO` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class TO(Node):
    """Represents TO Gerber extended command."""

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to(self)


class TO_UserName(TO):  # noqa: N801
    """Represents TO Gerber extended command with user name."""

    user_name: str
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_user_name(self)


class TO_N(TO):  # noqa: N801
    """Represents TO Gerber extended command with .N attribute."""

    net_names: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_n(self)


class TO_P(TO):  # noqa: N801
    """Represents TO Gerber extended command with .P attribute."""

    refdes: str
    number: str
    function: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_p(self)


class TO_C(TO):  # noqa: N801
    """Represents TO Gerber extended command with .C attribute."""

    refdes: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_c(self)


class TO_CRot(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CRot attribute."""

    angle: float

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_crot(self)


class TO_CMfr(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CMfr attribute."""

    manufacturer: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cmfr(self)


class TO_CMNP(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CMNP attribute."""

    part_number: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cmnp(self)


class TO_CVal(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CVal attribute."""

    value: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cval(self)


class Mount(Enum):
    """Mount type enumeration."""

    SMD = "SMD"
    TH = "TH"
    Pressfit = "Pressfit"
    Other = "Other"


class TO_CMnt(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CMnt attribute."""

    mount: Mount

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cmnt(self)


class TO_CFtp(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CFtp attribute."""

    footprint: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cftp(self)


class TO_CPgN(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CPgN attribute."""

    name: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cpgn(self)


class TO_CPgD(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CPgD attribute."""

    description: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_cpgd(self)


class TO_CHgt(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CHgt attribute."""

    height: float

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_chgt(self)


class TO_CLbN(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CLbN attribute."""

    name: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_clbn(self)


class TO_CLbD(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CLbD attribute."""

    description: str

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_clbd(self)


class TO_CSup(TO):  # noqa: N801
    """Represents TO Gerber extended command with .CSup attribute."""

    supplier: str
    supplier_part: str

    other_suppliers: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_to_csup(self)
