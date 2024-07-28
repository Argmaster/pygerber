"""`pygerber.nodes.attributes.TF` module contains definition of `TF` class."""

from __future__ import annotations

import datetime  # noqa: TCH003
import hashlib
from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List, Literal, Optional

from pydantic import Field

from pygerber.gerberx3.ast.nodes.base import Node

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.visitor import AstVisitor


class TF(Node):
    """Represents TF Gerber extended command."""

    @abstractmethod
    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""


class TF_UserName(TF):  # noqa: N801
    """Represents TF Gerber extended command with user name."""

    user_name: str
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_user_name(self)


class Part(Enum):
    """Enumerate supported part types."""

    Single = "Single"
    Array = "Array"
    FabricationPanel = "FabricationPanel"
    Coupon = "Coupon"
    Other = "Other"


class TF_Part(TF):  # noqa: N801
    """Represents TF Gerber extended command with part attribute."""

    part: Part
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_part(self)


class FileFunction(Enum):
    """Enumerate supported file function types."""

    Copper = "Copper"
    Plated = "Plated"
    NonPlated = "NonPlated"
    Profile = "Profile"
    Soldermask = "Soldermask"
    Legend = "Legend"
    Component = "Component"
    Paste = "Paste"
    Glue = "Glue"
    Carbonmask = "Carbonmask"
    Goldmask = "Goldmask"
    Heatsinkmask = "Heatsinkmask"
    Peelablemask = "Peelablemask"
    Silvermask = "Silvermask"
    Tinmask = "Tinmask"
    Depthrout = "Depthrout"
    Vcut = "Vcut"
    Viafill = "Viafill"
    Pads = "Pads"
    Other = "Other"
    Drillmap = "Drillmap"
    FabricationDrawing = "FabricationDrawing"
    Vcutmap = "Vcutmap"
    AssemblyDrawing = "AssemblyDrawing"
    ArrayDrawing = "ArrayDrawing"
    OtherDrawing = "OtherDrawing"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"

    __str__ = __repr__


class TF_FileFunction(TF):  # noqa: N801
    """Represents TF Gerber extended command with file function attribute."""

    file_function: FileFunction
    fields: List[str] = Field(default_factory=list)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_file_function(self)


class TF_FilePolarity(TF):  # noqa: N801
    """Represents TF Gerber extended command with file polarity attribute."""

    polarity: Literal["Positive", "Negative"]

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_file_polarity(self)


class TF_SameCoordinates(TF):  # noqa: N801
    """Represents TF Gerber extended command with same coordinates attribute."""

    identifier: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_same_coordinates(self)


class TF_CreationDate(TF):  # noqa: N801
    """Represents TF Gerber extended command with creation date attribute."""

    creation_date: datetime.datetime

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_creation_date(self)


class TF_GenerationSoftware(TF):  # noqa: N801
    """Represents TF Gerber extended command with generation software attribute."""

    vendor: Optional[str] = Field(default=None)
    application: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_generation_software(self)


class TF_ProjectId(TF):  # noqa: N801
    """Represents TF Gerber extended command with project id attribute."""

    name: Optional[str] = Field(default=None)
    guid: Optional[str] = Field(default=None)
    revision: Optional[str] = Field(default=None)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_project_id(self)


MD5_LENGTH_HEX = 32


class TF_MD5(TF):  # noqa: N801
    """Represents TF Gerber extended command with MD5 attribute."""

    md5: str = Field(min_length=MD5_LENGTH_HEX, max_length=MD5_LENGTH_HEX)

    def visit(self, visitor: AstVisitor) -> None:
        """Handle visitor call."""
        visitor.on_tf_md5(self)

    def check_source_hash(self) -> bool:
        """Validate MD5 attribute."""
        source = (
            self.source[: self.location - 1]
            .replace("\n", "")
            .replace("\r", "")
            .encode("utf-8")
        )
        source_hash = hashlib.md5(source).hexdigest()  # noqa: S324
        return source_hash == self.md5
