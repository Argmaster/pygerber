"""`pygerber.nodes.attribute.TA` module contains definition of `TA` class."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Callable, List, Literal, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerberx3.ast.visitor import AstVisitor


class TA(Node):
    """Represents TA Gerber extended command."""


class TA_UserName(TA):  # noqa: N801
    """Represents TA Gerber extended command with user name."""

    user_name: str
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_user_name(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_user_name


class AperFunction(Enum):
    """Enum representing possible AperFunction values."""

    ViaDrill = "ViaDrill"
    BackDrill = "BackDrill"
    ComponentDrill = "ComponentDrill"
    MechanicalDrill = "MechanicalDrill"
    CastellatedDrill = "CastellatedDrill"
    OtherDrill = "OtherDrill"
    ComponentPad = "ComponentPad"
    SMDPad = "SMDPad"
    BGAPad = "BGAPad"
    ConnectorPad = "ConnectorPad"
    HeatsinkPad = "HeatsinkPad"
    ViaPad = "ViaPad"
    TestPad = "TestPad"
    CastellatedPad = "CastellatedPad"
    FiducialPad = "FiducialPad"
    ThermalReliefPad = "ThermalReliefPad"
    WasherPad = "WasherPad"
    AntiPad = "AntiPad"
    OtherPad = "OtherPad"
    Conductor = "Conductor"
    EtchedComponent = "EtchedComponent"
    NonConductor = "NonConductor"
    CopperBalancing = "CopperBalancing"
    Border = "Border"
    OtherCopper = "OtherCopper"
    ComponentMain = "ComponentMain"
    ComponentOutline = "ComponentOutline"
    ComponentPin = "ComponentPin"
    Profile = "Profile"
    Material = "Material"
    NonMaterial = "NonMaterial"
    Other = "Other"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    __str__ = __repr__


class TA_AperFunction(TA):  # noqa: N801
    """Represents TA .AperFunction Gerber attribute."""

    function: Optional[AperFunction] = Field(default=None)
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_aper_function(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_aper_function


class TA_DrillTolerance(TA):  # noqa: N801
    """Represents TA .DrillTolerance Gerber attribute."""

    plus_tolerance: Optional[float] = Field(default=None)
    minus_tolerance: Optional[float] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_drill_tolerance(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_drill_tolerance


class TA_FlashText(TA):  # noqa: N801
    """Represents TA .FlashText Gerber attribute."""

    string: str
    mode: Literal["B", "C"]
    mirroring: Literal["R", "M"] = Field(default="R")
    font: Optional[str] = Field(default=None)
    size: Optional[str] = Field(default=None)
    comments: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_ta_flash_text(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], None]:
        """Get callback function for the node."""
        return visitor.on_ta_flash_text