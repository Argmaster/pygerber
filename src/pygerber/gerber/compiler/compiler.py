"""The `compiler` module contains implementation of compiler for transforming Gerber
abstract syntax tree to PyGerber rendering VM commands (RVMC).
"""

from __future__ import annotations

import math
import time
from math import cos, radians, sin
from typing import TYPE_CHECKING, ClassVar, Optional

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.expression_eval_visitor import ExpressionEvalVisitor
from pygerber.gerber.ast.nodes import (
    AB,
    ADC,
    ADO,
    ADP,
    ADR,
    D01,
    D03,
    ADmacro,
    Assignment,
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
from pygerber.gerber.ast.nodes.aperture.SR import SR
from pygerber.gerber.ast.nodes.types import ApertureIdStr, Double
from pygerber.gerber.ast.state_tracking_visitor import (
    StateTrackingVisitor,
)
from pygerber.gerber.compiler.errors import (
    ContourBufferNotSetError,
    CyclicBufferDependencyError,
    MacroNotDefinedError,
)
from pygerber.vm.commands import (
    Command,
    EndLayer,
    Line,
    PasteLayer,
    Shape,
    ShapeSegment,
    StartLayer,
)
from pygerber.vm.commands.shape_segments.arc import Arc
from pygerber.vm.rvmc import RVMC
from pygerber.vm.types import Box, LayerID, Matrix3x3, Vector
from pygerber.vm.vm import DrawCmdT

if TYPE_CHECKING:
    from typing_extensions import Protocol

    class _ArcFactory(Protocol):
        def __call__(
            self,
            start: tuple[float, float],
            end: tuple[float, float],
            center: tuple[float, float],
            thickness: float,
            *,
            is_negative: bool,
        ) -> Shape: ...


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
        self._contour_buffer: Optional[list[ShapeSegment]] = []
        self._create_main_buffer()

    def _set_buffer(self, buffer: CommandBuffer) -> None:
        """Register buffer."""
        self._buffers[buffer.id_str] = buffer

    def _get_buffer(self, id_: str) -> CommandBuffer:
        """Get buffer by id."""
        return self._buffers[id_]

    def _del_buffer(self, id_: str) -> None:
        """Delete buffer by id."""
        del self._buffers[id_]

    def _get_buffer_opt(self, id_: str) -> Optional[CommandBuffer]:
        """Get buffer by id."""
        return self._buffers.get(id_)

    def _get_current_buffer(self) -> CommandBuffer:
        return self._get_buffer(self._buffer_stack[-1])

    def _append_shape_to_current_buffer(self, command: Shape) -> None:
        self._get_current_buffer().append_shape(command)

    def _append_paste_to_current_buffer(self, command: PasteLayer) -> None:
        self._get_current_buffer().append_paste(command)

    def _expand_buffer_to_current_buffer(self, buffer: CommandBuffer) -> None:
        for command in buffer.commands:
            if isinstance(command, Shape):
                self._append_shape_to_current_buffer(command)
            elif isinstance(command, PasteLayer):
                self._append_paste_to_current_buffer(command)
            else:
                raise NotImplementedError(type(command))

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
        self._set_buffer(buffer)
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

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` node."""
        aperture_buffer = self._create_aperture_buffer(node.open.aperture_id)
        self._push_buffer(aperture_buffer.id_str)

        super().on_ab(node)

        self._pop_buffer()

        return node

    def on_sr(self, node: SR) -> SR:
        """Handle `SR` node."""
        aperture_buffer = self._create_aperture_buffer(
            ApertureIdStr(f"%%SR%{id(node)}%{time.time():.0f}")
        )
        self._push_buffer(aperture_buffer.id_str)

        super().on_sr(node)

        self._pop_buffer()

        buffer = self._get_buffer(aperture_buffer.id_str)

        x_delta = node.open.x_delta
        y_delta = node.open.y_delta

        for x in range(node.open.x_repeats):
            for y in range(node.open.y_repeats):
                x_coordinate = self.coordinate_x + (x * x_delta)
                y_coordinate = self.coordinate_y + (y * y_delta)
                tmp_buffer = self._apply_transform_to_buffer_non_recursive_tmp(
                    buffer, Matrix3x3.new_translate(x=x_coordinate, y=y_coordinate)
                )

                self._expand_buffer_to_current_buffer(tmp_buffer)

        self._del_buffer(aperture_buffer.id_str)
        return node

    def on_adc(self, node: ADC) -> ADC:
        """Handle `AD` circle node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_circle(
                (0.0, 0.0),
                node.diameter,
                is_negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.diameter),
                    is_negative=True,
                )
            )
        return node

    def _create_aperture_buffer(self, aperture_id: ApertureIdStr) -> CommandBuffer:
        buffer = CommandBuffer(
            aperture_id,
            box=None,
            origin=Vector(x=0, y=0),
            commands=[],
            depends_on=set(),
            resolved_dependencies=[],
        )
        self._set_buffer(buffer)

        return buffer

    def on_adr(self, node: ADR) -> ADR:
        """Handle `AD` rectangle node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_rectangle(
                (0.0, 0.0),
                node.width,
                node.height,
                is_negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.width, node.height),
                    is_negative=True,
                )
            )
        return node

    def on_ado(self, node: ADO) -> ADO:
        """Handle `AD` obround node."""
        self.on_ad(node)
        aperture_buffer = self._create_aperture_buffer(node.aperture_id)

        aperture_buffer.append_shape(
            Shape.new_obround(
                (0.0, 0.0),
                node.width,
                node.height,
                is_negative=False,
            )
        )
        if node.hole_diameter is not None and node.hole_diameter > 0:
            aperture_buffer.append_shape(
                Shape.new_circle(
                    (0.0, 0.0),
                    min(node.hole_diameter, node.width, node.height),
                    is_negative=True,
                )
            )
        return node

    def on_adp(self, node: ADP) -> ADP:
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
                    is_negative=True,
                )
            )
        return node

    def on_ad_macro(self, node: ADmacro) -> ADmacro:
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

        macro.visit(MacroEvalVisitor(self, aperture_buffer, scope))
        return node

    def on_draw_line(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in linear interpolation mode."""
        start_x = self.state.current_x
        start_y = self.state.current_y
        start_point = (start_x, start_y)

        end_x = self.coordinate_x
        end_y = self.coordinate_y
        end_point = (end_x, end_y)

        thickness = self._get_line_thickness(
            Vector.from_tuple((self.coordinate_x, self.coordinate_y))
        )
        self._append_shape_to_current_buffer(
            Shape.new_circle(
                start_point,
                thickness,
                is_negative=self.is_negative,
            )
        )
        self._append_shape_to_current_buffer(
            Shape.new_line(
                start_point,
                end_point,
                thickness=thickness,
                is_negative=self.is_negative,
            ),
        )
        self._append_shape_to_current_buffer(
            Shape.new_circle(
                end_point,
                thickness,
                is_negative=self.is_negative,
            )
        )

    def on_draw_cw_arc_mq(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in clockwise circular interpolation multi quadrant mode."""
        self._on_draw_arc_mq(Shape.new_cw_arc)

    def _on_draw_arc_mq(self, factory_method: _ArcFactory) -> None:
        start_x = self.state.current_x
        start_y = self.state.current_y
        start_point = (start_x, start_y)

        end_x = self.coordinate_x
        end_y = self.coordinate_y
        end_point = (end_x, end_y)

        center_x = start_x + self.coordinate_i
        center_y = start_y + self.coordinate_j
        center = (center_x, center_y)

        thickness = self._get_line_thickness(
            Vector.from_tuple((self.coordinate_x, self.coordinate_y))
        )

        self._append_shape_to_current_buffer(
            Shape.new_circle(
                start_point,
                thickness,
                is_negative=self.is_negative,
            )
        )
        if start_point == end_point:
            length = Vector(x=self.coordinate_i, y=self.coordinate_j).length()
            start_point = (center_x - length, center_y)
            end_point = (center_x + length, center_y)

            self._append_shape_to_current_buffer(
                factory_method(
                    start_point,
                    end_point,
                    center,
                    thickness,
                    is_negative=self.is_negative,
                )
            )
            self._append_shape_to_current_buffer(
                factory_method(
                    end_point,
                    start_point,
                    center,
                    thickness,
                    is_negative=self.is_negative,
                )
            )

        else:
            self._append_shape_to_current_buffer(
                factory_method(
                    start_point,
                    end_point,
                    center,
                    thickness,
                    is_negative=self.is_negative,
                )
            )
        self._append_shape_to_current_buffer(
            Shape.new_circle(
                end_point,
                thickness,
                is_negative=self.is_negative,
            )
        )

    def on_draw_ccw_arc_mq(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in counter-clockwise circular interpolation multi quadrant
        mode.
        """
        self._on_draw_arc_mq(Shape.new_ccw_arc)

    def on_start_region(self) -> None:
        """Handle start of region."""
        super().on_start_region()
        self._contour_buffer = []

    def on_in_region_draw_line(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in linear interpolation mode in region."""
        if self._contour_buffer is None:
            raise ContourBufferNotSetError

        start_x = self.state.current_x
        start_y = self.state.current_y
        start_point = (start_x, start_y)

        end_x = self.coordinate_x
        end_y = self.coordinate_y
        end_point = (end_x, end_y)

        self._contour_buffer.append(Line.from_tuples(start_point, end_point))

    def on_in_region_draw_cw_arc_mq(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in clockwise circular interpolation multi quadrant mode
        within region statement.
        """
        self._on_in_region_draw_arc_mq(is_clockwise=True)

    def _on_in_region_draw_arc_mq(self, *, is_clockwise: bool) -> None:
        if self._contour_buffer is None:
            raise ContourBufferNotSetError

        start_x = self.state.current_x
        start_y = self.state.current_y
        start_point = (start_x, start_y)

        end_x = self.coordinate_x
        end_y = self.coordinate_y
        end_point = (end_x, end_y)

        center_x = start_x + self.coordinate_i
        center_y = start_y + self.coordinate_j
        center = (center_x, center_y)

        if start_point == end_point:
            end_point = (center_x + self.coordinate_i, center_y + self.coordinate_j)

            self._contour_buffer.append(
                Arc.from_tuples(
                    start_point,
                    end_point,
                    center,
                    clockwise=is_clockwise,
                )
            )
            self._contour_buffer.append(
                Arc.from_tuples(
                    end_point,
                    start_point,
                    center,
                    clockwise=is_clockwise,
                )
            )

        else:
            self._contour_buffer.append(
                Arc.from_tuples(
                    start_point,
                    end_point,
                    center,
                    clockwise=is_clockwise,
                )
            )

    def on_in_region_draw_ccw_arc_mq(self, node: D01) -> None:  # noqa: ARG002
        """Handle `D01` node in counter-clockwise circular interpolation multi quadrant
        mode within region statement.
        """
        self._on_in_region_draw_arc_mq(is_clockwise=False)

    def on_flush_region(self) -> None:
        """Handle flush region after D02 command or after G37."""
        if self._contour_buffer is None:
            raise ContourBufferNotSetError

        if len(self._contour_buffer) > 0:
            self._append_shape_to_current_buffer(
                Shape(commands=self._contour_buffer, is_negative=self.is_negative)
            )

        self._contour_buffer = []

    def on_end_region(self) -> None:
        """Handle end of region."""
        super().on_end_region()
        self._contour_buffer = None

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
        transform = self.state.transform

        mirroring_matrix = Matrix3x3.new_reflect(**transform.mirroring.kwargs)
        rotation_matrix = Matrix3x3.new_rotate(transform.rotation)
        scale_matrix = Matrix3x3.new_scale(transform.scaling, transform.scaling)

        transform_matrix = mirroring_matrix @ rotation_matrix @ scale_matrix

        return self._get_buffer_with_transform(aperture_id, transform_matrix)

    def _get_buffer_with_transform(
        self, aperture_id: str, transform_matrix: Matrix3x3
    ) -> CommandBuffer:
        layer_id = f"{aperture_id}%{transform_matrix.tag}"
        buffer = self._get_buffer_opt(layer_id)

        if buffer is None:
            aperture_base_buffer = self._get_buffer(aperture_id)
            buffer = self._apply_transform_to_buffer(
                aperture_base_buffer, layer_id, transform_matrix
            )
            assert buffer.id_str == layer_id
            self._set_buffer(buffer)

        return buffer

    def _apply_transform_to_buffer(
        self, buffer: CommandBuffer, layer_id: str, transform_matrix: Matrix3x3
    ) -> CommandBuffer:
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
        aperture_id = aperture.open.aperture_id
        buffer = self._get_aperture_buffer(aperture_id)
        tmp_buffer = self._apply_transform_to_buffer_non_recursive_tmp(
            buffer, Matrix3x3.new_translate(x=self.coordinate_x, y=self.coordinate_y)
        )

        self._expand_buffer_to_current_buffer(tmp_buffer)

    def _apply_transform_to_buffer_non_recursive_tmp(
        self, buffer: CommandBuffer, transform_matrix: Matrix3x3
    ) -> CommandBuffer:
        commands: list[DrawCmdT] = []
        depends_on: set[str] = set()

        for cmd in buffer.commands:
            if isinstance(cmd, Shape):
                commands.append(cmd.transform(transform_matrix))

            elif isinstance(cmd, PasteLayer):
                depends_on.add(cmd.source_layer_id.id)
                commands.append(
                    PasteLayer(
                        source_layer_id=cmd.source_layer_id,
                        center=cmd.center.transform(transform_matrix),
                        is_negative=cmd.is_negative,
                    )
                )

            else:
                raise NotImplementedError(type(cmd))

        return CommandBuffer(
            "%temporary%",
            None,
            origin=buffer.origin,
            commands=commands,
            depends_on=depends_on,
            resolved_dependencies=[],
        )

    def _resolve_buffer_submit_order(self) -> list[CommandBuffer]:
        buffer_submit_order: list[str] = []

        def _(buffer: CommandBuffer) -> None:
            for dependency_id in buffer.depends_on:
                dependency = self._get_buffer(dependency_id)
                _(dependency)

                if buffer.id_str in buffer_submit_order:
                    raise CyclicBufferDependencyError(buffer, dependency)

            buffer_submit_order.append(buffer.id_str)

        _(self._get_buffer(self.MAIN_BUFFER_ID))

        return [self._get_buffer(id_) for id_ in buffer_submit_order]

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
        self,
        compiler: Compiler,
        aperture_buffer: CommandBuffer,
        scope: dict[str, Double],
    ) -> None:
        self._compiler = compiler
        self._aperture_buffer = aperture_buffer
        self._scope = scope
        self._expression_eval = ExpressionEvalVisitor(self._scope)

    def _eval(self, node: Expression) -> float:
        return self._expression_eval.evaluate(node)

    def on_code_1(self, node: Code1) -> Code1:
        """Handle `Code1` node."""
        exposure = self._eval(node.exposure)
        diameter = self._eval(node.diameter)
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        rotation = self._eval(node.rotation) if node.rotation is not None else None

        shape = Shape.new_circle(
            (center_x, center_y),
            diameter,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)
        return node

    def on_code_2(self, node: Code2) -> Code2:
        """Handle `Code2` node."""
        self._on_vector_line(node)
        return node

    def _on_vector_line(self, node: Code2 | Code20) -> None:
        exposure = self._eval(node.exposure)
        width = self._eval(node.width)
        start = (self._eval(node.start_x), self._eval(node.start_y))
        end = (self._eval(node.end_x), self._eval(node.end_y))
        rotation = self._eval(node.rotation)

        shape = Shape.new_line(
            start,
            end,
            thickness=width,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)

    def on_code_4(self, node: Code4) -> Code4:
        """Handle `Code4` node."""
        exposure = self._eval(node.exposure)
        start = (self._eval(node.start_x), self._eval(node.start_y))
        points = [(self._eval(point.x), self._eval(point.y)) for point in node.points]
        rotation = self._eval(node.rotation)

        shape = Shape.new_connected_points(
            start,
            *points,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)
        return node

    def on_code_5(self, node: Code5) -> Code5:
        """Handle `Code5` node."""
        exposure = self._eval(node.exposure)
        number_of_vertices = int(self._eval(node.number_of_vertices))
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        diameter = self._eval(node.diameter)
        rotation = self._eval(node.rotation)

        shape = Shape.new_polygon(
            (center_x, center_y),
            diameter,
            number_of_vertices,
            rotation,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)
        return node

    def on_code_6(self, node: Code6) -> Code6:
        """Handle `Code6` node."""
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        outer_diameter = self._eval(node.outer_diameter)
        ring_thickness = self._eval(node.ring_thickness)
        gap_between_rings = self._eval(node.gap_between_rings)
        max_ring_count = self._eval(node.max_ring_count)
        crosshair_thickness = self._eval(node.crosshair_thickness)
        crosshair_length = self._eval(node.crosshair_length)
        rotation = self._eval(node.rotation)

        center = (center_x, center_y)

        shapes: list[Shape] = []
        half_crosshair_length = crosshair_length / 2

        if crosshair_length > 0 and crosshair_thickness > 0:
            shapes.append(
                Shape.new_line(
                    (center_x, center_y - half_crosshair_length),
                    (center_x, center_y + half_crosshair_length),
                    crosshair_thickness,
                    is_negative=False,
                )
            )
            shapes.append(
                Shape.new_line(
                    (center_x - half_crosshair_length, center_y),
                    (center_x + half_crosshair_length, center_y),
                    crosshair_thickness,
                    is_negative=False,
                )
            )

        if ring_thickness > 0 and outer_diameter > 0 and max_ring_count > 0:
            diameter_delta = (gap_between_rings * 2) + (ring_thickness * 2)

            current_outer_diameter = outer_diameter
            # Diameter is reduced from both sides, hence ring_thickness * 2.
            current_inner_diameter = outer_diameter - (ring_thickness * 2)

            for _ in range(int(max_ring_count)):
                if current_outer_diameter <= ring_thickness:
                    shapes.append(
                        Shape.new_circle(
                            center, current_outer_diameter, is_negative=False
                        )
                    )
                    break

                shapes.extend(
                    Shape.new_ring(
                        center,
                        current_outer_diameter,
                        current_inner_diameter,
                        is_negative=False,
                    )
                )
                current_outer_diameter -= diameter_delta
                current_inner_diameter -= diameter_delta

        if rotation is not None:
            matrix = Matrix3x3.new_rotate(rotation)
            shapes = [shape.transform(matrix) for shape in shapes]

        for shape in shapes:
            self._aperture_buffer.append_shape(shape)

        return node

    def on_code_7(self, node: Code7) -> Code7:
        """Handle `Code7` node."""
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        outer_diameter = self._eval(node.outer_diameter)
        inner_diameter = self._eval(node.inner_diameter)

        if inner_diameter >= outer_diameter:
            return node

        gap_thickness = self._eval(node.gap_thickness)
        rotation = self._eval(node.rotation)

        thickness = outer_diameter - inner_diameter

        if gap_thickness * math.sqrt(2) >= inner_diameter:
            return node

        if thickness <= 0:
            return node

        aperture_id = ApertureIdStr(f"%%Code7%{id(node)}%{time.time():.0f}")
        aperture_buffer = self._compiler._create_aperture_buffer(  # noqa: SLF001
            aperture_id
        )

        shapes: list[Shape] = []
        shapes.extend(
            Shape.new_ring((0, 0), outer_diameter, inner_diameter, is_negative=False)
        )

        # Compensate rounding errors with rotation.
        radius_delta = outer_diameter / 2 + thickness / 1.99
        shapes.append(
            Shape.new_line(
                (0 - radius_delta, 0),
                (0 + radius_delta, 0),
                thickness=gap_thickness,
                is_negative=True,
            )
        )
        shapes.append(
            Shape.new_line(
                (0, 0 - radius_delta),
                (0, 0 + radius_delta),
                thickness=gap_thickness,
                is_negative=True,
            )
        )

        paste_center = Vector(x=center_x, y=center_y)

        if rotation is not None:
            matrix = Matrix3x3.new_rotate(rotation)
            shapes = [shape.transform(matrix) for shape in shapes]
            paste_center = paste_center.transform(matrix)

        for shape in shapes:
            aperture_buffer.append_shape(shape)

        self._aperture_buffer.append_paste(
            PasteLayer.new(
                source_layer_id=aperture_id,
                center=paste_center.xy,
                is_negative=False,
            )
        )
        return node

    def on_code_20(self, node: Code20) -> Code20:
        """Handle `Code20` node."""
        self._on_vector_line(node)
        return node

    def on_code_21(self, node: Code21) -> Code21:
        """Handle `Code21` node."""
        exposure = self._eval(node.exposure)
        width = self._eval(node.width)
        height = self._eval(node.height)
        center_x = self._eval(node.center_x)
        center_y = self._eval(node.center_y)
        rotation = self._eval(node.rotation)

        shape = Shape.new_rectangle(
            (center_x, center_y),
            width,
            height,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)
        return node

    def on_code_22(self, node: Code22) -> Code22:
        """Handle `Code22` node."""
        exposure = self._eval(node.exposure)
        width = self._eval(node.width)
        height = self._eval(node.height)
        x_lower_left = self._eval(node.x_lower_left)
        y_lower_left = self._eval(node.y_lower_left)
        rotation = self._eval(node.rotation)

        shape = Shape.new_rectangle(
            (x_lower_left + (width / 2), y_lower_left + (height / 2)),
            width,
            height,
            is_negative=(exposure == 0),
        )
        if rotation is not None:
            shape = shape.transform(Matrix3x3.new_rotate(rotation))

        self._aperture_buffer.append_shape(shape)
        return node

    def on_assignment(self, node: Assignment) -> Assignment:
        """Handle `Assignment` node."""
        self._scope[node.variable.variable] = self._eval(node.expression)
        return node
