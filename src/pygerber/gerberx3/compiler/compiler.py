"""`pygerber.gerberx3.compiler.compiler` module contains implementation of compiler for
transforming Gerber (AST) to PyGerber rendering VM commands (RVMC).
"""

from __future__ import annotations

from math import cos, radians, sin
from typing import Optional

from pygerber.gerberx3.ast.nodes import ADC, ADO, ADP, ADR, D01, D03, File
from pygerber.gerberx3.ast.state_tracking_visitor import (
    StateTrackingVisitor,
)
from pygerber.gerberx3.compiler.errors import CyclicBufferDependencyError
from pygerber.vm.commands import Command, PasteLayer, Shape
from pygerber.vm.commands.layer import EndLayer, StartLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types import Matrix3x3, Vector
from pygerber.vm.types.box import AutoBox, FixedBox
from pygerber.vm.types.layer_id import LayerID
from pygerber.vm.vm import DrawCmdT


class CommandBuffer:
    """Container for commands and metadata about relations with other containers."""

    def __init__(
        self,
        id_: str,
        box: Optional[AutoBox | FixedBox] = None,
        commands: Optional[list[DrawCmdT]] = None,
        depends_on: Optional[set[str]] = None,
        resolved_dependencies: Optional[list[CommandBuffer]] = None,
    ) -> None:
        self.id_str = id_
        self.commands: list[DrawCmdT] = [] if commands is None else commands
        self.box = AutoBox() if box is None else box
        self.depends_on: set[str] = set() if depends_on is None else depends_on
        self.resolved_dependencies: list[CommandBuffer] = (
            [] if resolved_dependencies is None else resolved_dependencies
        )

    @property
    def layer_id(self) -> LayerID:
        """Get layer id."""
        return LayerID(id=self.id_str)

    def append_shape(self, command: Shape) -> None:
        """Append command to buffer."""
        self.commands.append(command)

    def append_paste(self, command: PasteLayer) -> None:
        """Append command to buffer."""
        self.depends_on.add(command.source_layer_id.id)
        self.commands.append(command)


class Compiler(StateTrackingVisitor):
    """Compiler for transforming transforming Gerber (AST) to PyGerber rendering VM
    commands (RVMC).
    """

    def __init__(self, *, ignore_program_stop: bool = False) -> None:
        super().__init__(ignore_program_stop=ignore_program_stop)
        self._buffers: dict[str, CommandBuffer] = {}
        self._buffer_stack: list[str] = []
        self._create_buffer("%main%")
        self._push_buffer("%main%")

        self._aperture_buffers: dict[str, CommandBuffer] = {}

    def _get_current_buffer(self) -> CommandBuffer:
        return self._buffers[self._buffer_stack[-1]]

    def _append_shape_to_current_buffer(self, command: Shape) -> None:
        self._get_current_buffer().append_shape(command)

    def _append_paste_to_current_buffer(self, command: PasteLayer) -> None:
        self._get_current_buffer().append_paste(command)

    def _create_buffer(self, id_: str) -> CommandBuffer:
        buffer = CommandBuffer(id_)
        self._buffers[id_] = buffer
        return buffer

    def _push_buffer(self, id_: str) -> None:
        self._buffer_stack.append(id_)

    def _pop_buffer(self) -> None:
        self._buffer_stack.pop()

    def _get_line_thickness(self, line_direction: Vector) -> float:
        current_aperture = self.state.current_aperture
        if isinstance(current_aperture, ADC):
            return current_aperture.diameter

        if isinstance(current_aperture, (ADR, ADO)):
            angle = line_direction.angle_between(Vector.unit.x)
            sin_angle = sin(radians(-angle))
            cos_angle = cos(radians(-angle))

            return Vector(
                x=current_aperture.width * cos_angle,
                y=current_aperture.height * sin_angle,
            ).length()

        if isinstance(current_aperture, ADP):
            return current_aperture.outer_diameter

        raise NotImplementedError(type(current_aperture))

    def on_adc(self, node: ADC) -> None:
        """Handle `AD` circle node."""
        self.on_ad(node)
        buffer = CommandBuffer(
            node.aperture_id,
            box=AutoBox(center_override=Vector(x=0.0, y=0.0)),
        )
        self._aperture_buffers[node.aperture_id] = buffer

        buffer.append_shape(
            Shape.new_circle(
                (0.0, 0.0),
                node.diameter,
                negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    node.hole_diameter,
                    negative=True,
                )
            )

    def on_adr(self, node: ADR) -> None:
        """Handle `AD` rectangle node."""
        self.on_ad(node)

    def on_ado(self, node: ADO) -> None:
        """Handle `AD` obround node."""
        self.on_ad(node)

    def on_adp(self, node: ADP) -> None:
        """Handle `AD` polygon node."""
        self.on_ad(node)

    def on_draw_line(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in linear interpolation mode."""
        thickness = self._get_line_thickness(
            Vector.from_tuple((self.coordinate_x, self.coordinate_y))
        )
        self._append_shape_to_current_buffer(
            Shape.new_circle(
                (self.state.current_x, self.state.current_y),
                thickness,
                negative=self.is_negative,
            )
        )
        self._append_shape_to_current_buffer(
            Shape.new_line(
                (self.state.current_x, self.state.current_y),
                (self.coordinate_x, self.coordinate_y),
                thickness=thickness,
                negative=self.is_negative,
            ),
        )
        self._append_shape_to_current_buffer(
            Shape.new_circle(
                (self.coordinate_x, self.coordinate_y),
                thickness,
                negative=self.is_negative,
            )
        )

    def on_flash_circle(self, node: D03, aperture: ADC) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADC` aperture."""
        buffer = self._get_aperture_buffer(aperture.aperture_id)

        self._append_paste_to_current_buffer(
            PasteLayer(
                source_layer_id=buffer.layer_id,
                center=Vector(x=self.coordinate_x, y=self.coordinate_y),
                is_negative=self.is_negative,
            ),
        )

    def _get_aperture_buffer(self, aperture_id: str) -> CommandBuffer:
        layer_id = f"{aperture_id}%{self.state.transform.tag}"
        buffer = self._buffers.get(layer_id)

        if buffer is None:
            aperture_base_buffer = self._aperture_buffers[aperture_id]
            buffer = self._transform_buffer(aperture_base_buffer)
            self._buffers[layer_id] = buffer

        return buffer

    def _transform_buffer(self, buffer: CommandBuffer) -> CommandBuffer:
        """Create new buffer with applied transformation."""
        layer_id = f"{buffer.id_str}%{self.state.transform.tag}"
        transform = self.state.transform
        is_negative = self.is_negative

        mirroring_matrix = Matrix3x3.new_reflect(**transform.mirroring.kwargs)
        rotation_matrix = Matrix3x3.new_rotate(transform.rotation)
        scale_matrix = Matrix3x3.new_scale(transform.scaling, transform.scaling)

        transform_matrix = mirroring_matrix @ rotation_matrix @ scale_matrix

        commands: list[DrawCmdT] = []
        depends_on: set[str] = set()

        for c in buffer.commands:
            if isinstance(c, Shape):
                commands.append(
                    c.transform(transform_matrix).model_copy(
                        update={"negative": is_negative}
                    )
                )

            elif isinstance(c, PasteLayer):
                aperture_buffer = self._get_aperture_buffer(c.source_layer_id.id)
                depends_on.add(aperture_buffer.id_str)
                commands.append(
                    PasteLayer(
                        source_layer_id=LayerID(id=aperture_buffer.id_str),
                        center=c.center.transform(transform_matrix),
                        is_negative=is_negative,
                    )
                )

            else:
                raise NotImplementedError(type(c))

        return CommandBuffer(
            layer_id,
            AutoBox(center_override=buffer.box.center),
            commands=commands,
            depends_on=depends_on,
            resolved_dependencies=[],
        )

    def on_flash_rectangle(self, node: D03, aperture: ADR) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADC` aperture."""
        self._append_shape_to_current_buffer(
            Shape.new_rectangle(
                (self.coordinate_x, self.coordinate_y),
                aperture.width,
                aperture.height,
                negative=self.is_negative,
            )
        )

    def on_flash_obround(self, node: D03, aperture: ADO) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADO` aperture."""
        self._append_shape_to_current_buffer(
            Shape.new_obround(
                (self.coordinate_x, self.coordinate_y),
                aperture.width,
                aperture.height,
                negative=self.is_negative,
            )
        )

    def _resolve_buffer_submit_order(self) -> list[CommandBuffer]:
        buffer_submit_order: list[CommandBuffer] = []

        for buffer in self._buffers.values():
            for dependency in buffer.depends_on:
                buffer.resolved_dependencies.append(self._buffers[dependency])

        def _(buffer: CommandBuffer) -> None:
            for dependency in buffer.resolved_dependencies:
                _(dependency)

            if buffer in buffer_submit_order:
                raise CyclicBufferDependencyError(buffer, dependency)

            buffer_submit_order.append(buffer)

        _(self._buffers["%main%"])

        return buffer_submit_order

    def _convert_buffers_to_rvmc(self) -> RVMC:
        commands: list[Command] = []
        buffer_submit_order = self._resolve_buffer_submit_order()

        for buffer in buffer_submit_order:
            commands.append(StartLayer(id=LayerID(id=buffer.id_str), box=buffer.box))
            commands.extend(buffer.commands)
            commands.append(EndLayer())

        return RVMC(commands)

    def compile(self, ast: File) -> RVMC:
        """Compile Gerber AST to RVMC."""
        ast.visit(self)

        return self._convert_buffers_to_rvmc()
