"""`` package contains all the node classes used to represent
the Gerber X3 abstract syntax tree.
"""

from __future__ import annotations

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.errors import (
    ApertureNotFoundError,
    ApertureNotSelectedError,
    AstError,
    CoordinateFormatNotSetError,
    DirectADHandlerDispatchNotSupportedError,
    PackedCoordinateTooLongError,
    PackedCoordinateTooShortError,
    SourceNotAvailableError,
    VisitorError,
)
from pygerber.gerber.ast.expression_eval_visitor import ExpressionEvalVisitor
from pygerber.gerber.ast.node_finder import NodeFinder
from pygerber.gerber.ast.nodes import File
from pygerber.gerber.ast.state_tracking_visitor import (
    ApertureStorage,
    ArcInterpolation,
    Attributes,
    CoordinateFormat,
    ImageAttributes,
    PlotMode,
    ProgramStop,
    State,
    StateTrackingVisitor,
    Transform,
)

__all__ = [
    "AstVisitor",
    "AstError",
    "VisitorError",
    "StateTrackingVisitor",
    "DirectADHandlerDispatchNotSupportedError",
    "ApertureNotSelectedError",
    "ApertureNotFoundError",
    "SourceNotAvailableError",
    "CoordinateFormatNotSetError",
    "PackedCoordinateTooLongError",
    "PackedCoordinateTooShortError",
    "ExpressionEvalVisitor",
    "NodeFinder",
    "State",
    "CoordinateFormat",
    "Attributes",
    "ImageAttributes",
    "Transform",
    "PlotMode",
    "ArcInterpolation",
    "ApertureStorage",
    "ProgramStop",
]


def get_final_state(ast: File) -> State:
    visitor = StateTrackingVisitor()
    ast.visit(visitor)
    return visitor.state
