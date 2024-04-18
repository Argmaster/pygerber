"""Container for diagnostic info."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any, List, Optional, Union

from pydantic import Field

from pygerber.common.frozen_general_model import FrozenGeneralModel
from pygerber.common.position import Position
from pygerber.gerberx3.language_server._internals import (
    IS_LANGUAGE_SERVER_FEATURE_AVAILABLE,
)

if TYPE_CHECKING:
    import lsprotocol.types as lspt

if IS_LANGUAGE_SERVER_FEATURE_AVAILABLE:
    import lsprotocol.types as lspt


class Location(FrozenGeneralModel):
    """Represents a location inside a resource, such as a line
    inside a text file.
    """

    uri: str

    range: Range

    def __repr__(self) -> str:
        return f"{self.uri}:{self.range!r}"

    def to_lspt(self) -> lspt.Location:
        """Convert to corresponding language server protocol type."""
        return lspt.Location(uri=self.uri, range=self.range.to_lspt())


class DiagnosticRelatedInformation(FrozenGeneralModel):
    """Represents a related message and source code location for a diagnostic. This
    should be used to point to code locations that cause or related to a diagnostics,
    e.g when duplicating a symbol in a scope.
    """

    location: Location
    """The location of this related diagnostic information."""

    message: str
    """The message of this related diagnostic information."""

    def to_lspt(self) -> lspt.DiagnosticRelatedInformation:
        """Convert to corresponding language server protocol type."""
        return lspt.DiagnosticRelatedInformation(
            location=self.location.to_lspt(),
            message=self.message,
        )


class CodeDescription(FrozenGeneralModel):
    """Structure to capture a description for an error code.

    @since 3.16.0
    """

    # Since: 3.16.0

    href: str
    """An URI to open with more information about the diagnostic error."""

    def to_lspt(self) -> lspt.CodeDescription:
        """Convert to corresponding language server protocol type."""
        return lspt.CodeDescription(href=self.href)


@enum.unique
class DiagnosticSeverity(int, enum.Enum):
    """The diagnostic's severity."""

    Error = 1
    """Reports an error."""
    Warning = 2
    """Reports a warning."""
    Information = 3
    """Reports an information."""
    Hint = 4
    """Reports a hint."""

    def to_lspt(self) -> lspt.DiagnosticSeverity:
        """Convert to corresponding language server protocol type."""
        return lspt.DiagnosticSeverity(self.value)


class Range(FrozenGeneralModel):
    """A range in a text document expressed as (zero-based) start and end positions.

    If you want to specify a range that contains a line including the line ending
    character(s) then use an end position denoting the start of the next line.
    For example:
    ```ts
    {
        start: { line: 5, character: 23 }
        end : { line 6, character : 0 }
    }
    ```
    """

    start: Position
    """The range's start position."""

    end: Position
    """The range's end position."""

    def __repr__(self) -> str:
        return f"{self.start!r}-{self.end!r}"

    def to_lspt(self) -> lspt.Range:
        """Convert to corresponding language server protocol type."""
        return lspt.Range(start=self.start.to_lspt(), end=self.end.to_lspt())


@enum.unique
class DiagnosticTag(int, enum.Enum):
    """The diagnostic tags.

    @since 3.15.0
    """

    # Since: 3.15.0
    Unnecessary = 1
    """Unused or unnecessary code.

    Clients are allowed to render diagnostics with this tag faded out instead of having
    an error squiggle."""
    Deprecated = 2
    """Deprecated or obsolete code.

    Clients are allowed to rendered diagnostics with this tag strike through."""

    def to_lspt(self) -> lspt.DiagnosticTag:
        """Convert to corresponding language server protocol type."""
        return lspt.DiagnosticTag(self.value)


class Diagnostic(FrozenGeneralModel):
    """Represents a diagnostic, such as a compiler error or warning. Diagnostic objects
    are only valid in the scope of a resource.
    """

    range: Range
    """The range at which the message applies"""

    message: str
    """The diagnostic's message. It usually appears in the user interface"""

    severity: Optional[DiagnosticSeverity] = Field(default=None)
    """The diagnostic's severity. Can be omitted. If omitted it is up to the
    client to interpret diagnostics as error, warning, info or hint."""

    code: Optional[Union[int, str]] = Field(default=None)
    """The diagnostic's code, which usually appear in the user interface."""

    code_description: Optional[CodeDescription] = Field(default=None)
    """An optional property to describe the error code.
    Requires the code field (above) to be present/not null.

    @since 3.16.0"""
    # Since: 3.16.0

    source: Optional[str] = Field(default=None)
    """A human-readable string describing the source of this
    diagnostic, e.g. 'typescript' or 'super lint'. It usually
    appears in the user interface."""

    tags: Optional[List[DiagnosticTag]] = Field(default=None)
    """Additional metadata about the diagnostic.

    @since 3.15.0"""
    # Since: 3.15.0

    related_information: Optional[List[DiagnosticRelatedInformation]] = Field(
        default=None,
    )
    """An array of related diagnostic information, e.g. when symbol-names within
    a scope collide all definitions can be marked via this property."""

    data: Optional[Any] = Field(default=None)
    """A data entry field that is preserved between a `textDocument/publishDiagnostics`
    notification and `textDocument/codeAction` request.

    @since 3.16.0"""

    def to_lspt(self) -> lspt.Diagnostic:
        """Repack into language server protocol type."""
        return lspt.Diagnostic(
            range=self.range.to_lspt(),
            message=self.message,
            severity=(
                lspt.DiagnosticSeverity(self.severity.value) if self.severity else None
            ),
            code=self.code,
            code_description=(
                self.code_description.to_lspt() if self.code_description else None
            ),
            source=self.source,
            tags=[t.to_lspt() for t in self.tags] if self.tags is not None else None,
            related_information=(
                [i.to_lspt() for i in self.related_information]
                if self.related_information is not None
                else None
            ),
        )
