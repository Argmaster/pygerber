"""`pygerber.gerberx3.compiler.compiler` module contains implementation of compiler for
transforming Gerber (AST) to PyGerber rendering VM commands (RVMC).
"""

from __future__ import annotations

from math import cos, radians, sin
from typing import ClassVar, Optional

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.expression_eval_visitor import ExpressionEvalVisitor
from pygerber.gerberx3.ast.nodes import (
    AB,
    ADC,
    ADO,
    ADP,
    ADR,
    D01,
    D03,
    ADmacro,
    Code0,
    Code1,
    Code2,
    Code4,
    Code5,
    Code6,
    Code7,
    Code20,
    Code21,
    Code22,
    Expression,
    File,
)
from pygerber.gerberx3.ast.nodes.math.assignment import Assignment
from pygerber.gerberx3.ast.nodes.types import ApertureIdStr, Double
from pygerber.gerberx3.ast.state_tracking_visitor import (
    StateTrackingVisitor,
)
from pygerber.gerberx3.compiler.errors import (
    CyclicBufferDependencyError,
    MacroNotDefinedError,
)
from pygerber.vm.commands import Command, EndLayer, PasteLayer, Shape, StartLayer
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types import Box, LayerID, Matrix3x3, Vector
from pygerber.vm.vm import DrawCmdT


class CommandBuffer:
    """Container for commands and metadata about relations with other containers."""

    def __init__(
        self,
        id_: str,
        box: Optional[Box],
        origin: Vector,
        commands: list[DrawCmdT],
        depends_on: set[str],
        resolved_dependencies: list[CommandBuffer],
    ) -> None:
        self.id_str = id_
        self.commands = commands
        self.box = box
        self.origin = origin
        self.depends_on = depends_on
        self.resolved_dependencies = resolved_dependencies

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

    MAIN_BUFFER_ID: ClassVar[str] = "%main%"

    def __init__(self, *, ignore_program_stop: bool = False) -> None:
        super().__init__(ignore_program_stop=ignore_program_stop)
        self._buffers: dict[str, CommandBuffer] = {}
        self._buffer_stack: list[str] = []
        self._create_main_buffer()

        self._aperture_buffers: dict[str, CommandBuffer] = {}

    def _get_current_buffer(self) -> CommandBuffer:
        return self._buffers[self._buffer_stack[-1]]

    def _append_shape_to_current_buffer(self, command: Shape) -> None:
        self._get_current_buffer().append_shape(command)

    def _append_paste_to_current_buffer(self, command: PasteLayer) -> None:
        self._get_current_buffer().append_paste(command)

    def _create_main_buffer(self) -> CommandBuffer:
        buffer = CommandBuffer(
            self.MAIN_BUFFER_ID,
            box=None,
            origin=Vector(x=0, y=0),
            commands=[],
            depends_on=set(),
            resolved_dependencies=[],
        )
        assert self.MAIN_BUFFER_ID not in self._buffers
        self._buffers[self.MAIN_BUFFER_ID] = buffer
        self._push_buffer(self.MAIN_BUFFER_ID)

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
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_circle(
                (0.0, 0.0),
                node.diameter,
                negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.diameter),
                    negative=True,
                )
            )

    def _create_aperture_buffer(self, aperture_id: ApertureIdStr) -> CommandBuffer:
        buffer = CommandBuffer(
            aperture_id,
            box=None,
            origin=Vector(x=0, y=0),
            commands=[],
            depends_on=set(),
            resolved_dependencies=[],
        )
        self._aperture_buffers[aperture_id] = buffer

        return buffer

    def on_adr(self, node: ADR) -> None:
        """Handle `AD` rectangle node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_rectangle(
                (0.0, 0.0),
                node.width,
                node.height,
                negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.width, node.height),
                    negative=True,
                )
            )

    def on_ado(self, node: ADO) -> None:
        """Handle `AD` obround node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_obround(
                (0.0, 0.0),
                node.width,
                node.height,
                negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.width, node.height),
                    negative=True,
                )
            )

    def on_adp(self, node: ADP) -> None:
        """Handle `AD` polygon node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_polygon(
                (0.0, 0.0),
                node.outer_diameter,
                node.vertices,
                node.rotation or 0.0,
                is_negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.outer_diameter),
                    negative=True,
                )
            )

    def on_ad_macro(self, node: ADmacro) -> None:
        """Handle `AD` macro node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        if node.params is None:
            scope = {}
        else:
            scope = {f"${i + 1}": param for i, param in enumerate(node.params)}

        macro = self.state.apertures.macros.get(node.name)
        if macro is None:
            raise MacroNotDefinedError(node.name)

        macro.visit(MacroEvalVisitor(aperture_buffer, scope))

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
        self._on_flash_aperture(aperture.aperture_id)

    def _on_flash_aperture(self, aperture_id: ApertureIdStr) -> None:
        buffer = self._get_aperture_buffer(aperture_id)

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

        mirroring_matrix = Matrix3x3.new_reflect(**transform.mirroring.kwargs)
        rotation_matrix = Matrix3x3.new_rotate(transform.rotation)
        scale_matrix = Matrix3x3.new_scale(transform.scaling, transform.scaling)

        transform_matrix = mirroring_matrix @ rotation_matrix @ scale_matrix

        commands: list[DrawCmdT] = []
        depends_on: set[str] = set()

        for cmd in buffer.commands:
            if isinstance(cmd, Shape):
                commands.append(cmd.transform(transform_matrix))

            elif isinstance(cmd, PasteLayer):
                aperture_buffer = self._get_aperture_buffer(cmd.source_layer_id.id)
                depends_on.add(aperture_buffer.id_str)
                commands.append(
                    PasteLayer(
                        source_layer_id=LayerID(id=aperture_buffer.id_str),
                        center=cmd.center.transform(transform_matrix),
                        is_negative=cmd.is_negative,
                    )
                )

            else:
                raise NotImplementedError(type(cmd))

        return CommandBuffer(
            layer_id,
            None,
            origin=buffer.origin,
            commands=commands,
            depends_on=depends_on,
            resolved_dependencies=[],
        )

    def on_flash_rectangle(self, node: D03, aperture: ADR) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADC` aperture."""
        self._on_flash_aperture(aperture.aperture_id)

    def on_flash_obround(self, node: D03, aperture: ADO) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADO` aperture."""
        self._on_flash_aperture(aperture.aperture_id)

    def on_flash_polygon(self, node: D03, aperture: ADP) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADP` aperture."""
        self._on_flash_aperture(aperture.aperture_id)

    def on_flash_macro(self, node: D03, aperture: ADmacro) -> None:  # noqa: ARG002
        """Handle `D03` node with `ADM` aperture."""
        self._on_flash_aperture(aperture.aperture_id)

    def on_flash_block(self, node: D03, aperture: AB) -> None:  # noqa: ARG002
        """Handle `D03` node with `AB` aperture."""
        self._on_flash_aperture(aperture.open.aperture_id)

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

        _(self._buffers[self.MAIN_BUFFER_ID])

        return buffer_submit_order

    def _convert_buffers_to_rvmc(self) -> RVMC:
        commands: list[Command] = []
        buffer_submit_order = self._resolve_buffer_submit_order()

        for buffer in buffer_submit_order:
            commands.append(StartLayer(id=LayerID(id=buffer.id_str), box=buffer.box))
            commands.extend(buffer.commands)
            commands.append(EndLayer())

        return RVMC(commands=commands)

    def compile(self, ast: File) -> RVMC:
        """Compile Gerber AST to RVMC."""
        ast.visit(self)

        return self._convert_buffers_to_rvmc()


class MacroEvalVisitor(AstVisitor):
    """Visitor for evaluating macro primitives."""

    def __init__(
        self, aperture_buffer: CommandBuffer, scope: dict[str, Double]
    ) -> None:
        self._aperture_buffer = aperture_buffer
        self._scope = scope
        self._expression_eval = ExpressionEvalVisitor(self._scope)

    def _eval(self, node: Expression) -> float:
        return self._expression_eval.evaluate(node)

    def on_code_0(self, node: Code0) -> None:
        """Handle `Code0` node."""

    def on_code_1(self, node: Code1) -> None:
        """Handle `Code1` node."""
        exposure = self._eval(node.exposure)
        diameter = self._eval(node.diameter)
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        rotation = self._eval(node.rotation) if node.rotation is not None else None

        shape = Shape.new_circle(
            (center_x, center_y),
            diameter,
            negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)

    def on_code_2(self, node: Code2) -> None:
        """Handle `Code2` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        node.end_x.visit(self)
        node.end_y.visit(self)
        node.rotation.visit(self)

    def on_code_4(self, node: Code4) -> None:
        """Handle `Code4` node."""
        node.exposure.visit(self)
        node.number_of_points.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        for point in node.points:
            point.visit(self)
        node.rotation.visit(self)

    def on_code_5(self, node: Code5) -> None:
        """Handle `Code5` node."""
        node.exposure.visit(self)
        node.number_of_vertices.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.diameter.visit(self)
        node.rotation.visit(self)

    def on_code_6(self, node: Code6) -> None:
        """Handle `Code6` node."""
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.outer_diameter.visit(self)
        node.ring_thickness.visit(self)
        node.gap_between_rings.visit(self)
        node.max_ring_count.visit(self)
        node.crosshair_thickness.visit(self)
        node.crosshair_length.visit(self)
        node.rotation.visit(self)

    def on_code_7(self, node: Code7) -> None:
        """Handle `Code7` node."""
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.outer_diameter.visit(self)
        node.inner_diameter.visit(self)
        node.gap_thickness.visit(self)
        node.rotation.visit(self)

    def on_code_20(self, node: Code20) -> None:
        """Handle `Code20` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        node.end_x.visit(self)
        node.end_y.visit(self)
        node.rotation.visit(self)

    def on_code_21(self, node: Code21) -> None:
        """Handle `Code21` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.height.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.rotation.visit(self)

    def on_code_22(self, node: Code22) -> None:
        """Handle `Code22` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.height.visit(self)
        node.x_lower_left.visit(self)
        node.y_lower_left.visit(self)
        node.rotation.visit(self)

    def on_assignment(self, node: Assignment) -> None:
        """Handle `Assignment` node."""
        self._scope[node.variable.variable] = self._eval(node.expression)
