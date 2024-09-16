from __future__ import annotations

from contextlib import contextmanager, suppress
from io import StringIO
from typing import Generator

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.nodes import M02, File, Node
from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
from pygerber.gerberx3.ast.state_tracking_visitor import (
    PlotMode,
    ProgramStop,
    StateTrackingVisitor,
)
from pygerber.gerberx3.formatter import Formatter
from pygerber.gerberx3.spec import rev_2024_05 as spec


class LimitedStateTrackingVisitor(StateTrackingVisitor):
    """The `LimitedStateTrackingVisitor` class which stops AST walk before particular
    location in source.
    """

    def __init__(self, max_location: int) -> None:
        super().__init__()
        self.max_location = max_location

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        with suppress(ProgramStop):
            try:
                for command in node.nodes:
                    source_info = command.source_info
                    assert source_info is not None

                    if source_info.end_location > self.max_location:
                        raise ProgramStop(M02())

                    try:
                        command.visit(self)
                    except Exception as e:
                        if self.on_exception(command, e):
                            raise
            finally:
                self.on_end_of_file(node)

        return node


class GerberHoverCreator(AstVisitor):
    """The `GerberHoverCreator` class generates hover information for Gerber AST
    node.
    """

    def __init__(self, ast: File) -> None:
        super().__init__()
        self.ast = ast
        self.hover_markdown: StringIO

    def create_hover_markdown(self, node: Node) -> str:
        """Get hover markdown for the given node."""
        self.hover_markdown = StringIO()

        source_info = node.source_info
        assert source_info is not None

        visitor = LimitedStateTrackingVisitor(source_info.location)
        self.ast.visit(visitor)

        self.state = visitor.state

        node.visit(self)

        return self.hover_markdown.getvalue()

    def _sep(self) -> None:
        self.hover_markdown.write("\n---\n")

    @contextmanager
    def _code_block(self, language: str) -> Generator[None, None, None]:
        self.hover_markdown.write(f"```{language}\n")
        yield
        self.hover_markdown.write("```\n")

    def on_d01(self, node: D01) -> D01:
        with self._code_block("gerber"):
            Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._sep()
        self.hover_markdown.write(
            f"Uses aperture: `{self.state.current_aperture_id}`\n"
        )

        self._sep()
        self.hover_markdown.write(f"Plot mode: `{self.state.plot_mode.name}`\n")

        self._sep()
        self.hover_markdown.write(
            f"Interpolation mode: `{self.state.arc_interpolation.name}`\n"
        )

        fmt = self.state.coordinate_format
        if fmt is not None:
            self._sep()
            self.hover_markdown.write(
                f"Starts at: (`{self.state.current_x}`, `{self.state.current_y}`)\n"
            )
            self._sep()

            end_x = (
                fmt.unpack_x(node.x.value)
                if node.x is not None
                else self.state.current_x
            )
            end_y = (
                fmt.unpack_y(node.y.value)
                if node.y is not None
                else self.state.current_y
            )
            self.hover_markdown.write(f"Ends at: (`{end_x}`, `{end_y}`)\n")

            if self.state.plot_mode != PlotMode.LINEAR:
                end_i = fmt.unpack_x(node.i.value) if node.i is not None else 0.0
                end_j = fmt.unpack_y(node.j.value) if node.j is not None else 0.0
                self.hover_markdown.write(
                    f"Arc center offset: (`{end_i}`, `{end_j}`)\n"
                )

        self._sep()
        self.hover_markdown.write(spec.d01())

        return node
