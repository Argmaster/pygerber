from __future__ import annotations

import base64
import io
from contextlib import contextmanager, suppress
from io import StringIO
from typing import TYPE_CHECKING, Generator, Optional, cast

from pygerber.gerber import formatter
from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes import (
    AD,
    ADC,
    ADO,
    ADP,
    ADR,
    D01,
    D02,
    D03,
    FS,
    G01,
    G02,
    G74,
    G75,
    LM,
    LR,
    LS,
    M02,
    MO,
    TA,
    TD,
    TF,
    TO,
    TO_C,
    TO_CMNP,
    TO_N,
    TO_P,
    ADmacro,
    Code1,
    Code2,
    Code20,
    Coordinate,
    CoordinateX,
    CoordinateY,
    Dnn,
    File,
    Node,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
    TO_CFtp,
    TO_CHgt,
    TO_CLbD,
    TO_CLbN,
    TO_CMfr,
    TO_CMnt,
    TO_CPgD,
    TO_CPgN,
    TO_CRot,
    TO_CSup,
    TO_CVal,
    TO_UserName,
)
from pygerber.gerber.ast.nodes.enums import Mirroring, Polarity
from pygerber.gerber.ast.state_tracking_visitor import (
    ArcInterpolation,
    PlotMode,
    ProgramStop,
    StateTrackingVisitor,
)
from pygerber.gerber.compiler import compile
from pygerber.gerber.spec import rev_2024_05 as spec
from pygerber.vm import render
from pygerber.vm.pillow import PillowResult

if TYPE_CHECKING:
    from PIL import Image


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


class ToMarkdown(AstVisitor):
    """Convert Gerber Node to markdown."""

    def __init__(self) -> None:
        super().__init__()
        self.markdown: StringIO

    def to_markdown(self, node: Node) -> str:
        """Convert Gerber Node to markdown."""
        self.markdown = StringIO()
        node.visit(self)
        return self.markdown.getvalue()

    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:
        """Handle `TA_UserName` node."""
        fields_md = ", ".join(f"`{f}`" for f in node.fields)
        self.markdown.write(f"`{node.attribute_name}`: {fields_md}")
        return node

    def on_ta_aper_function(self, node: TA_AperFunction) -> TA_AperFunction:
        """Handle `TA_AperFunction` node."""
        function = node.function.value if node.function else "<missing>"
        fields_md = ", ".join(f"`{f}`" for f in node.fields)
        self.markdown.write(f"`{node.attribute_name}`: `{function}`")
        if node.fields:
            self.markdown.write(f", ({fields_md})")

        return node

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> TA_DrillTolerance:
        """Handle `TA_DrillTolerance` node."""
        self.markdown.write(
            f"`{node.attribute_name}`: `+{node.plus_tolerance}` /"
            f" -`{node.minus_tolerance}`"
        )

        return node

    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:
        """Handle `TA_FlashText` node."""
        string = node.string.replace("`", "'")
        self.markdown.write(f"`{node.attribute_name}`: `{string}`")
        return node

    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:
        """Handle `TO_UserName` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(", ".join(f"`{f}`" for f in node.fields))
        return node

    def on_to_n(self, node: TO_N) -> TO_N:
        """Handle `TO_N` node."""
        self.markdown.write(f"`CAD net name` (`{node.attribute_name}`): ")
        self.markdown.write(", ".join(f"`{f}`" for f in node.net_names))
        return node

    def on_to_p(self, node: TO_P) -> TO_P:
        """Handle `TO_P` node`."""
        self.markdown.write(f"`Pin number` (`{node.attribute_name}`): ")
        self.markdown.write(f"`{node.refdes}`, `{node.number}`, `{node.function}`")
        return node

    def on_to_c(self, node: TO_C) -> TO_C:
        """Handle `TO_C` node."""
        self.markdown.write(
            f"`Component reference designator({node.attribute_name}`): "
        )
        self.markdown.write(f"`{node.refdes}`")
        return node

    def on_to_crot(self, node: TO_CRot) -> TO_CRot:
        """Handle `TO_CRot` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.angle}°`")
        return node

    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:
        """Handle `TO_CMfr` node."""
        self.markdown.write(f"`Supplier` (`{node.attribute_name}`): ")
        self.markdown.write(f"`{node.manufacturer}`")
        return node

    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:
        """Handle `TO_CMNP` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.part_number}`")
        return node

    def on_to_cval(self, node: TO_CVal) -> TO_CVal:
        """Handle `TO_CVal` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.value}`")
        return node

    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:
        """Handle `TO_CVal` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.mount.name}`")
        return node

    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:
        """Handle `TO_Cftp` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.footprint}`")
        return node

    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:
        """Handle `TO_CPgN` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.name}`")
        return node

    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:
        """Handle `TO_CPgD` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.description}`")
        return node

    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:
        """Handle `TO_CHgt` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.height}`")
        return node

    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:
        """Handle `TO_CLbN` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.name}`")
        return node

    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:
        """Handle `TO_CLbD` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.description}`")
        return node

    def on_to_csup(self, node: TO_CSup) -> TO_CSup:
        """Handle `TO_CSup` node."""
        self.markdown.write(f"`{node.attribute_name}`: ")
        self.markdown.write(f"`{node.supplier}`, ")
        self.markdown.write(f"`{node.supplier_part}`")
        if node.other_suppliers:
            self.markdown.write(", ")
            self.markdown.write(", ".join(f"`{f}`" for f in node.other_suppliers))
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

    def _print(self, text: str) -> None:
        self.hover_markdown.write(text + " ")

    def _print_line(self, text: str = "", end: str = "\n") -> None:
        self.hover_markdown.write(text + end)

    def _single_break(self) -> None:
        self._print_line("<br/>\n")

    def _double_break(self) -> None:
        self._print_line("<br/><br/>\n")

    def _append_current_xy(self, message: str = "Starts at:") -> None:
        self._sep()
        self._print_line(
            f"{message} &nbsp; _x =_ `{self.state.current_x}` "
            f"_y =_ `{self.state.current_y}`"
        )

    def _append_xy(
        self,
        message: str,
        x: Optional[Coordinate],
        y: Optional[Coordinate],
        default_x: float = 0.0,
        default_y: float = 0.0,
    ) -> None:
        fmt = self.state.coordinate_format
        if fmt is None:
            return

        x_value = fmt.unpack_x(x.value) if x else default_x
        y_value = fmt.unpack_y(y.value) if y else default_y

        self._sep()
        self._print_line(
            f"{message} &nbsp;&nbsp;&nbsp; _x =_ `{x_value}` _y =_ `{y_value}`"
        )

    def _current_aperture(self) -> None:
        self._print(f"`Aperture: {self.state.current_aperture_id}`")

    def _arc_interpolation_mode(self) -> None:
        if self.state.plot_mode != PlotMode.LINEAR:
            self._print(
                {
                    ArcInterpolation.MULTI_QUADRANT: "`Multi-quadrant`",
                    ArcInterpolation.SINGLE_QUADRANT: "`Single-quadrant`",
                }[self.state.arc_interpolation]
            )

    def _plot_mode(self) -> None:
        self._print(
            {
                PlotMode.LINEAR: "`Linear`",
                PlotMode.ARC: "`Clockwise Arc`",
                PlotMode.CCW_ARC: "`Counter-clockwise Arc`",
            }[self.state.plot_mode]
        )

    def _polarity(self) -> None:
        self._print(
            {Polarity.Dark: "`Dark polarity`", Polarity.Clear: "`Clear polarity`"}[
                self.state.transform.polarity
            ]
        )

    def _transform(self) -> None:
        self._print(
            {
                Mirroring.NONE: "`No Mirroring`",
                Mirroring.X: "`Mirroring X`",
                Mirroring.Y: "`Mirroring Y`",
                Mirroring.XY: "`Mirroring X and Y`",
            }[self.state.transform.mirroring]
        )
        self._print(f"`Rotation: {self.state.transform.rotation}`°")
        self._print_line(f"`Scale: {self.state.transform.scaling}`")

    def _aperture_attributes(self, aperture_id: str) -> None:
        attributes = self.state.apertures.per_aperture_attributes.get(aperture_id, {})

        if len(attributes) == 0:
            return

        self._sep()
        self._print_line(f"### Aperture attributes (`{aperture_id}`)")

        serializer = ToMarkdown()

        for attr in attributes.values():
            self._print("-")
            self._print_line(serializer.to_markdown(attr))

        self._print_line()

    def _object_attributes(self) -> None:
        attributes = self.state.attributes.object_attributes

        if len(attributes) == 0:
            return

        self._sep()
        self._print_line("### Object attributes")

        serializer = ToMarkdown()

        for attr in attributes.values():
            self._print("-")
            self._print_line(serializer.to_markdown(attr))

        self._print_line()

    def _base64_image_tag(self, image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_bytes = buffered.getvalue()
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        return f'<p align="center"><img src="data:image/jpeg;base64,{encoded_image}" alt="Embedded Image" /></p>'

    def _visualize_draw_op(self, extra_commands: list[Node]) -> None:
        nodes: list[Node] = []
        assert self.state.coordinate_format is not None

        nodes.append(
            FS(
                zeros=self.state.coordinate_format.zeros,
                coordinate_mode=self.state.coordinate_format.coordinate_mode,
                x_integral=self.state.coordinate_format.x_integral,
                x_decimal=self.state.coordinate_format.x_decimal,
                y_integral=self.state.coordinate_format.y_integral,
                y_decimal=self.state.coordinate_format.y_decimal,
            )
        )

        nodes.append(MO(mode=self.state.unit_mode))
        nodes.append(
            D02(
                x=CoordinateX(
                    value=self.state.coordinate_format.pack_x(self.state.current_x)
                ),
                y=CoordinateY(
                    value=self.state.coordinate_format.pack_y(self.state.current_y)
                ),
            )
        )
        nodes.extend(self.state.apertures.macros.values())
        nodes.extend(self.state.apertures.apertures.values())
        nodes.extend(self.state.apertures.macros.values())

        nodes.append(
            {
                PlotMode.LINEAR: G01(),
                PlotMode.ARC: G02(),
                PlotMode.CCW_ARC: G02(),
            }[self.state.plot_mode]
        )
        nodes.append(
            {
                ArcInterpolation.MULTI_QUADRANT: G75(),
                ArcInterpolation.SINGLE_QUADRANT: G74(),
            }[self.state.arc_interpolation]
        )
        nodes.append(LM(mirroring=self.state.transform.mirroring))
        nodes.append(LS(scale=self.state.transform.scaling))
        nodes.append(LR(rotation=self.state.transform.rotation))

        if self.state.current_aperture_id is not None:
            nodes.append(
                Dnn(
                    aperture_id=self.state.current_aperture_id,
                )
            )
        nodes.extend(extra_commands)

        rvmc = compile(File(nodes=nodes))
        result = render(rvmc, dpmm=100)
        assert isinstance(result, PillowResult)

        tag = self._base64_image_tag(result.get_image())

        self._print_line(tag)

    def _spec_ref(self, bullets: str) -> None:
        self._sep()
        self._single_break()
        self._print_line(spec.spec_title())
        self._print_line(bullets)
        self._single_break()

    def on_d01(self, node: D01) -> D01:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._append_current_xy()
        self._append_xy(
            "Ends at:", node.x, node.y, self.state.current_x, self.state.current_y
        )

        if self.state.plot_mode != PlotMode.LINEAR:
            self._append_xy("Arc center at:", node.i, node.j)

        self._sep()
        self._current_aperture()
        self._arc_interpolation_mode()
        self._plot_mode()
        self._polarity()
        self._transform()

        if self.state.current_aperture_id:
            self._aperture_attributes(self.state.current_aperture_id)

        self._object_attributes()

        self._sep()
        self._print_line("### Visualization")
        self._single_break()
        self._visualize_draw_op([node])
        self._single_break()

        self._spec_ref(spec.d01())

        return node

    def on_d02(self, node: D02) -> D02:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._append_xy(
            "Relocate to:", node.x, node.y, self.state.current_x, self.state.current_y
        )

        self._spec_ref(spec.d02())

        return node

    def on_d03(self, node: D03) -> D03:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._append_xy(
            "Flash at:", node.x, node.y, self.state.current_x, self.state.current_y
        )

        self._sep()
        self._current_aperture()
        self._arc_interpolation_mode()
        self._plot_mode()
        self._polarity()
        self._transform()

        if self.state.current_aperture_id:
            self._aperture_attributes(self.state.current_aperture_id)

        self._object_attributes()

        self._sep()
        self._print_line("### Visualization")
        self._single_break()
        self._visualize_draw_op([node])
        self._single_break()

        self._spec_ref(spec.d03())

        return node

    def on_to(self, node: TO) -> None:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._spec_ref(spec.to())

    def on_ta(self, node: TA) -> None:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._spec_ref(spec.ta())

    def on_tf(self, node: TF) -> None:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._spec_ref(spec.tf())

    def on_td(self, node: TD) -> TD:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._spec_ref(spec.td())

        return node

    def on_dnn(self, node: Dnn) -> Dnn:
        with self._code_block("gerber"):
            formatter.Formatter().format(File(nodes=[node]), self.hover_markdown)

        self._aperture_attributes(node.aperture_id)

        self._object_attributes()

        if self.state.coordinate_format is not None:
            self._sep()
            self._print_line("### Visualization")
            self._single_break()
            self._visualize_draw_op(
                cast(
                    "list[Node]",
                    [
                        node,
                        D03(
                            x=CoordinateX(
                                value=self.state.coordinate_format.pack_x(0.0)
                            ),
                            y=CoordinateY(
                                value=self.state.coordinate_format.pack_y(0.0)
                            ),
                        ),
                    ],
                )
            )
            self._single_break()

        self._spec_ref(spec.dnn())
        return node

    def on_ad(self, node: AD) -> None:
        self._add_code_block_format_node(node)
        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

    def _add_code_block_format_node(self, node: Node) -> None:
        with self._code_block("gerber"):
            formatter.Formatter().format_node(node, self.hover_markdown)

    def _visualize_aperture_definition(self, node: AD) -> None:
        if self.state.coordinate_format is not None:
            self._sep()
            self._print_line("### Visualization")
            self._single_break()
            self._visualize_draw_op(
                cast(
                    "list[Node]",
                    [
                        node,
                        Dnn(aperture_id=node.aperture_id),
                        D03(
                            x=CoordinateX(
                                value=self.state.coordinate_format.pack_x(0.0)
                            ),
                            y=CoordinateY(
                                value=self.state.coordinate_format.pack_y(0.0)
                            ),
                        ),
                    ],
                )
            )
            self._single_break()

    def on_adc(self, node: ADC) -> ADC:
        self._add_code_block_format_node(node)

        self._print("\n - standard template: `Circle`")
        self._print(f"\n - diameter: `{node.diameter}`")
        self._print(f"\n - hole_diameter: `{node.hole_diameter}`")

        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

        self._spec_ref(spec.adc())

        return node

    def on_adr(self, node: ADR) -> ADR:
        self._add_code_block_format_node(node)

        self._print("\n - standard template: `Rectangle`")
        self._print(f"\n - width: `{node.width}`")
        self._print(f"\n - height: `{node.height}`")
        self._print(f"\n - hole_diameter: `{node.hole_diameter}`")

        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

        self._spec_ref(spec.adr())

        return node

    def on_ado(self, node: ADO) -> ADO:
        self._add_code_block_format_node(node)

        self._print("\n - standard template: `Obround`")
        self._print(f"\n - width: `{node.width}`")
        self._print(f"\n - height: `{node.height}`")
        self._print(f"\n - hole_diameter: `{node.hole_diameter}`")

        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

        self._spec_ref(spec.ado())

        return node

    def on_adp(self, node: ADP) -> ADP:
        self._add_code_block_format_node(node)

        self._print("\n - standard template: `Polygon`")
        self._print(f"\n - outer diameter: `{node.outer_diameter}`")
        self._print(f"\n - vertex count: `{node.vertices}`")
        self._print(f"\n - rotation: `{node.rotation or 0.0}°`")
        self._print(f"\n - hole_diameter: `{node.hole_diameter}`")

        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

        self._spec_ref(spec.adp())

        return node

    def on_ad_macro(self, node: ADmacro) -> ADmacro:
        self._add_code_block_format_node(node)

        self._print(f"\n - macro name: `{node.name}`")
        if node.params:
            for i, param in enumerate(node.params, start=1):
                self._print(f"\n - parameter `${i}`: `{param}`")

        self._aperture_attributes(node.aperture_id)
        self._visualize_aperture_definition(node)

        self._spec_ref(spec.ad_macro())

        return node

    def on_code_1(self, node: Code1) -> Code1:
        fmt = formatter.Formatter(
            formatter.Options(macro_split_mode=formatter.MacroSplitMode.NoSplit)
        )

        with self._code_block("gerber"):
            fmt.format_node(node, self.hover_markdown)
            self._print_line()

        self._print("\n - exposure: `")
        fmt.format_node(node.exposure, self.hover_markdown)

        self._print("`\n - diameter: `")
        fmt.format_node(node.diameter, self.hover_markdown)

        self._print("`\n - center_x: `")
        fmt.format_node(node.center_x, self.hover_markdown)

        self._print("`\n - center_y: `")
        fmt.format_node(node.center_y, self.hover_markdown)

        self._print("`\n - rotation: `")
        if node.rotation is not None:
            fmt.format_node(node.rotation, self.hover_markdown)
            self._print("°`\n")
        else:
            self._print_line("None`")

        self._spec_ref(spec.code_1())

        return node

    def on_code_2(self, node: Code2) -> Code2:
        fmt = formatter.Formatter(
            formatter.Options(macro_split_mode=formatter.MacroSplitMode.NoSplit)
        )

        with self._code_block("gerber"):
            fmt.format_node(node, self.hover_markdown)
            self._print_line()

        self._print("\n - exposure: `")
        fmt.format_node(node.exposure, self.hover_markdown)

        self._print("`\n - width: `")
        fmt.format_node(node.width, self.hover_markdown)

        self._print("`\n - start_x: `")
        fmt.format_node(node.start_x, self.hover_markdown)

        self._print("`\n - start_y: `")
        fmt.format_node(node.start_y, self.hover_markdown)

        self._print("`\n - end_x: `")
        fmt.format_node(node.end_x, self.hover_markdown)

        self._print("`\n - end_y: `")
        fmt.format_node(node.end_y, self.hover_markdown)

        self._print("`\n - rotation: `")
        fmt.format_node(node.rotation, self.hover_markdown)
        self._print("°`\n")

        self._spec_ref(spec.code_1())

        return node

    def on_code_20(self, node: Code20) -> Code20:
        return super().on_code_20(node)
