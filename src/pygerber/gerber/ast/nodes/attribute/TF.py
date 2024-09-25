"""`pygerber.nodes.attributes.TF` module contains definition of `TF` class."""

from __future__ import annotations

import datetime  # noqa: TCH003
import hashlib
from typing import TYPE_CHECKING, Callable, List, Literal, Optional

from pydantic import Field

from pygerber.gerber.ast.errors import SourceNotAvailableError
from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.enums import FileFunction, Part

if TYPE_CHECKING:
    from typing_extensions import Self

    from pygerber.gerber.ast.ast_visitor import AstVisitor


class TF(Node):
    """Represents TF Gerber extended command."""

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        raise NotImplementedError


class TF_UserName(TF):  # noqa: N801
    """Represents TF Gerber extended command with user name."""

    user_name: str
    fields: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return self.user_name

    def visit(self, visitor: AstVisitor) -> TF_UserName:
        """Handle visitor call."""
        return visitor.on_tf_user_name(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_UserName]:
        """Get callback function for the node."""
        return visitor.on_tf_user_name


class TF_Part(TF):  # noqa: N801
    """Represents TF Gerber extended command with part attribute."""

    part: Part
    fields: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".Part"

    def visit(self, visitor: AstVisitor) -> TF_Part:
        """Handle visitor call."""
        return visitor.on_tf_part(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_Part]:
        """Get callback function for the node."""
        return visitor.on_tf_part


class TF_FileFunction(TF):  # noqa: N801
    """Represents TF Gerber extended command with file function attribute."""

    file_function: FileFunction
    fields: List[str] = Field(default_factory=list)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".FileFunction"

    def visit(self, visitor: AstVisitor) -> TF_FileFunction:
        """Handle visitor call."""
        return visitor.on_tf_file_function(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_FileFunction]:
        """Get callback function for the node."""
        return visitor.on_tf_file_function


class TF_FilePolarity(TF):  # noqa: N801
    """Represents TF Gerber extended command with file polarity attribute."""

    polarity: Literal["Positive", "Negative"]

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".FilePolarity"

    def visit(self, visitor: AstVisitor) -> TF_FilePolarity:
        """Handle visitor call."""
        return visitor.on_tf_file_polarity(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_FilePolarity]:
        """Get callback function for the node."""
        return visitor.on_tf_file_polarity


class TF_SameCoordinates(TF):  # noqa: N801
    """Represents TF Gerber extended command with same coordinates attribute."""

    identifier: Optional[str] = Field(default=None)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".SameCoordinates"

    def visit(self, visitor: AstVisitor) -> TF_SameCoordinates:
        """Handle visitor call."""
        return visitor.on_tf_same_coordinates(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_SameCoordinates]:
        """Get callback function for the node."""
        return visitor.on_tf_same_coordinates


class TF_CreationDate(TF):  # noqa: N801
    """Represents TF Gerber extended command with creation date attribute."""

    creation_date: datetime.datetime

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".CreationDate"

    def visit(self, visitor: AstVisitor) -> TF_CreationDate:
        """Handle visitor call."""
        return visitor.on_tf_creation_date(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_CreationDate]:
        """Get callback function for the node."""
        return visitor.on_tf_creation_date


class TF_GenerationSoftware(TF):  # noqa: N801
    """Represents TF Gerber extended command with generation software attribute."""

    vendor: Optional[str] = Field(default=None)
    application: Optional[str] = Field(default=None)
    version: Optional[str] = Field(default=None)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".GenerationSoftware"

    def visit(self, visitor: AstVisitor) -> TF_GenerationSoftware:
        """Handle visitor call."""
        return visitor.on_tf_generation_software(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_GenerationSoftware]:
        """Get callback function for the node."""
        return visitor.on_tf_generation_software


class TF_ProjectId(TF):  # noqa: N801
    """Represents TF Gerber extended command with project id attribute."""

    name: Optional[str] = Field(default=None)
    guid: Optional[str] = Field(default=None)
    revision: Optional[str] = Field(default=None)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".ProjectId"

    def visit(self, visitor: AstVisitor) -> TF_ProjectId:
        """Handle visitor call."""
        return visitor.on_tf_project_id(self)

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_ProjectId]:
        """Get callback function for the node."""
        return visitor.on_tf_project_id


MD5_LENGTH_HEX = 32


class TF_MD5(TF):  # noqa: N801
    """Represents TF Gerber extended command with MD5 attribute."""

    md5: str = Field(min_length=MD5_LENGTH_HEX, max_length=MD5_LENGTH_HEX)

    @property
    def attribute_name(self) -> str:
        """Get attribute name."""
        return ".MD5"

    def visit(self, visitor: AstVisitor) -> TF_MD5:
        """Handle visitor call."""
        return visitor.on_tf_md5(self)

    def check_source_hash(self) -> bool:
        """Validate MD5 attribute."""
        if self.source_info is None:
            raise SourceNotAvailableError(self)

        source = (
            self.source_info.source[: self.source_info.location - 1]
            .replace("\n", "")
            .replace("\r", "")
            .encode("utf-8")
        )
        source_hash = hashlib.md5(source).hexdigest()  # noqa: S324
        return source_hash == self.md5

    def get_visitor_callback_function(
        self, visitor: AstVisitor
    ) -> Callable[[Self], TF_MD5]:
        """Get callback function for the node."""
        return visitor.on_tf_md5
