"""`pygerber.gerberx3.formatter` module contains implementation `Formatter` class
which implements configurable Gerber code formatting.
"""

from __future__ import annotations

from contextlib import contextmanager
from enum import Enum
from typing import TYPE_CHECKING, Generator, Literal, Optional

from pyparsing import cached_property

from pygerber.gerberx3.ast.nodes.types import Double
from pygerber.gerberx3.ast.visitor import AstVisitor

if TYPE_CHECKING:
    from io import StringIO

    from pygerber.gerberx3.ast.nodes.aperture.AB_close import ABclose
    from pygerber.gerberx3.ast.nodes.aperture.AB_open import ABopen
    from pygerber.gerberx3.ast.nodes.aperture.ADC import ADC
    from pygerber.gerberx3.ast.nodes.aperture.ADmacro import ADmacro
    from pygerber.gerberx3.ast.nodes.aperture.ADO import ADO
    from pygerber.gerberx3.ast.nodes.aperture.ADP import ADP
    from pygerber.gerberx3.ast.nodes.aperture.ADR import ADR
    from pygerber.gerberx3.ast.nodes.aperture.AM_close import AMclose
    from pygerber.gerberx3.ast.nodes.aperture.AM_open import AMopen
    from pygerber.gerberx3.ast.nodes.aperture.SR_close import SRclose
    from pygerber.gerberx3.ast.nodes.aperture.SR_open import SRopen
    from pygerber.gerberx3.ast.nodes.attribute.TA import (
        TA_AperFunction,
        TA_DrillTolerance,
        TA_FlashText,
        TA_UserName,
    )
    from pygerber.gerberx3.ast.nodes.attribute.TD import TD
    from pygerber.gerberx3.ast.nodes.attribute.TF import (
        TF_MD5,
        TF_CreationDate,
        TF_FileFunction,
        TF_FilePolarity,
        TF_GenerationSoftware,
        TF_Part,
        TF_ProjectId,
        TF_SameCoordinates,
        TF_UserName,
    )
    from pygerber.gerberx3.ast.nodes.attribute.TO import (
        TO_C,
        TO_CMNP,
        TO_N,
        TO_P,
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
    from pygerber.gerberx3.ast.nodes.d_codes.D01 import D01
    from pygerber.gerberx3.ast.nodes.d_codes.D02 import D02
    from pygerber.gerberx3.ast.nodes.d_codes.D03 import D03
    from pygerber.gerberx3.ast.nodes.d_codes.Dnn import Dnn
    from pygerber.gerberx3.ast.nodes.file import File
    from pygerber.gerberx3.ast.nodes.g_codes.G01 import G01
    from pygerber.gerberx3.ast.nodes.g_codes.G02 import G02
    from pygerber.gerberx3.ast.nodes.g_codes.G03 import G03
    from pygerber.gerberx3.ast.nodes.g_codes.G04 import G04
    from pygerber.gerberx3.ast.nodes.g_codes.G36 import G36
    from pygerber.gerberx3.ast.nodes.g_codes.G37 import G37
    from pygerber.gerberx3.ast.nodes.g_codes.G54 import G54
    from pygerber.gerberx3.ast.nodes.g_codes.G55 import G55
    from pygerber.gerberx3.ast.nodes.g_codes.G70 import G70
    from pygerber.gerberx3.ast.nodes.g_codes.G71 import G71
    from pygerber.gerberx3.ast.nodes.g_codes.G74 import G74
    from pygerber.gerberx3.ast.nodes.g_codes.G75 import G75
    from pygerber.gerberx3.ast.nodes.g_codes.G90 import G90
    from pygerber.gerberx3.ast.nodes.g_codes.G91 import G91
    from pygerber.gerberx3.ast.nodes.load.LM import LM
    from pygerber.gerberx3.ast.nodes.load.LN import LN
    from pygerber.gerberx3.ast.nodes.load.LP import LP
    from pygerber.gerberx3.ast.nodes.load.LR import LR
    from pygerber.gerberx3.ast.nodes.load.LS import LS
    from pygerber.gerberx3.ast.nodes.m_codes.M00 import M00
    from pygerber.gerberx3.ast.nodes.m_codes.M01 import M01
    from pygerber.gerberx3.ast.nodes.m_codes.M02 import M02
    from pygerber.gerberx3.ast.nodes.math.assignment import Assignment
    from pygerber.gerberx3.ast.nodes.math.constant import Constant
    from pygerber.gerberx3.ast.nodes.math.operators.binary.add import Add
    from pygerber.gerberx3.ast.nodes.math.operators.binary.div import Div
    from pygerber.gerberx3.ast.nodes.math.operators.binary.mul import Mul
    from pygerber.gerberx3.ast.nodes.math.operators.binary.sub import Sub
    from pygerber.gerberx3.ast.nodes.math.operators.unary.neg import Neg
    from pygerber.gerberx3.ast.nodes.math.operators.unary.pos import Pos
    from pygerber.gerberx3.ast.nodes.math.point import Point
    from pygerber.gerberx3.ast.nodes.math.variable import Variable
    from pygerber.gerberx3.ast.nodes.other.coordinate import (
        CoordinateI,
        CoordinateJ,
        CoordinateX,
        CoordinateY,
    )
    from pygerber.gerberx3.ast.nodes.primitives.code_0 import Code0
    from pygerber.gerberx3.ast.nodes.primitives.code_1 import Code1
    from pygerber.gerberx3.ast.nodes.primitives.code_2 import Code2
    from pygerber.gerberx3.ast.nodes.primitives.code_4 import Code4
    from pygerber.gerberx3.ast.nodes.primitives.code_5 import Code5
    from pygerber.gerberx3.ast.nodes.primitives.code_6 import Code6
    from pygerber.gerberx3.ast.nodes.primitives.code_7 import Code7
    from pygerber.gerberx3.ast.nodes.primitives.code_20 import Code20
    from pygerber.gerberx3.ast.nodes.primitives.code_21 import Code21
    from pygerber.gerberx3.ast.nodes.primitives.code_22 import Code22
    from pygerber.gerberx3.ast.nodes.properties.AS import AS
    from pygerber.gerberx3.ast.nodes.properties.FS import FS
    from pygerber.gerberx3.ast.nodes.properties.IN import IN
    from pygerber.gerberx3.ast.nodes.properties.IP import IP
    from pygerber.gerberx3.ast.nodes.properties.IR import IR
    from pygerber.gerberx3.ast.nodes.properties.MI import MI
    from pygerber.gerberx3.ast.nodes.properties.MO import MO
    from pygerber.gerberx3.ast.nodes.properties.OF import OF
    from pygerber.gerberx3.ast.nodes.properties.SF import SF


class FormatterError(Exception):
    """Formatter error."""


class Formatter(AstVisitor):
    """Gerber X3 compatible formatter."""

    class MacroSplitMode(Enum):
        """Macro split mode."""

        NONE = "none"
        PRIMITIVES = "primitives"
        PARAMETERS = "parameters"

    def __init__(  # noqa: PLR0913
        self,
        *,
        indent_character: Literal[" ", "\t"] = " ",
        macro_body_indent: str | int = 4,
        macro_param_indent: str | int = 4,
        macro_split_mode: MacroSplitMode = MacroSplitMode.PRIMITIVES,
        macro_end_in_new_line: bool = False,
        indent_block_aperture_body: str = "",
        indent_step_and_repeat: str = "",
        float_decimal_places: int = 6,
        float_trim_trailing_zeros: bool = True,
        indent_non_aperture_select_commands: bool = False,
        split_format_select: bool = False,
        split_aperture_definition: bool = False,
        split_extended_command_boundaries: bool = False,
        strip_whitespace: bool = False,
    ) -> None:
        r"""Initialize Formatter instance.

        Parameters
        ----------
        indent_character: Literal[" ", "\t"], optional
            Character used for indentation, by default " "
        macro_body_indent : str | int, optional
            Indentation of macro body, by default 4
        macro_param_indent: str | int, optional
            Indentation of macro parameters, by default 4
            This indentation is added on top of macro body indentation.
        macro_split_mode : Literal["none", "primitives", "parameters"], optional
            Changes how macro definitions are formatted, by default "none"
            When "none" is selected, macro will be formatted as a single line.
            ```gerber
            %AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*%
            ```
            When "primitives" is selected, macro will be formatted with each primitive
            on a new line.
            ```gerber
            %AMDonut*
            1,1,$1,$2,$3*
            $4=$1x0.75*
            1,0,$4,$2,$3*%
            ```
        macro_end_in_new_line: bool, optional
            _description_, by default False
        indent_block_aperture_body : str, optional
            _description_, by default ""
        indent_step_and_repeat : str, optional
            _description_, by default ""
        float_decimal_places : int, optional
            _description_, by default 6
        float_trim_trailing_zeros : bool, optional
            _description_, by default True
        indent_non_aperture_select_commands : bool, optional
            _description_, by default False
        split_format_select : bool, optional
            _description_, by default False
        split_aperture_definition : bool, optional
            _description_, by default False
        split_extended_command_boundaries : bool, optional
            _description_, by default False
        strip_whitespace : bool, optional
            _description_, by default False

        """
        super().__init__()
        self.indent_character = indent_character

        if isinstance(macro_body_indent, int):
            macro_body_indent = indent_character * macro_body_indent
        self.macro_body_indent = macro_body_indent

        if isinstance(macro_param_indent, int):
            macro_param_indent = indent_character * macro_param_indent
        self.macro_param_indent = macro_param_indent

        self.macro_split_mode = macro_split_mode
        self.macro_end_in_new_line = macro_end_in_new_line

        self.indent_block_aperture_body = indent_block_aperture_body
        self.indent_step_and_repeat = indent_step_and_repeat
        self.float_decimal_places = float_decimal_places

        self.float_trim_trailing_zeros = float_trim_trailing_zeros
        self.indent_non_aperture_select_commands = indent_non_aperture_select_commands
        self.split_format_select = split_format_select
        self.split_aperture_definition = split_aperture_definition
        self.split_extended_command_boundaries = split_extended_command_boundaries
        self.strip_whitespace = strip_whitespace

        self._output: Optional[StringIO] = None

    def format(self, source: File, output: StringIO) -> None:
        """Format Gerber AST according to rules specified in Formatter constructor."""
        self._output = output
        try:
            self.on_file(source)
        finally:
            self._output = None

    @property
    def output(self) -> StringIO:
        """Get output buffer."""
        if self._output is None:
            msg = "Output buffer is not set."
            raise FormatterError(msg)

        return self._output

    def _fmt_double(self, value: Double) -> str:
        double = f"{value:.{self.float_decimal_places}f}"
        if self.float_trim_trailing_zeros:
            return double.rstrip("0").rstrip(".")
        return double

    @cached_property
    def lf(self) -> str:
        """Get end of line character."""
        return "" if self.strip_whitespace else "\n"

    @contextmanager
    def _command(self, cmd: str) -> Generator[None, None, None]:
        self._write(cmd)
        yield
        self._write(f"*{self.lf}")

    @contextmanager
    def _extended_command(self, cmd: str) -> Generator[None, None, None]:
        self._write(f"%{cmd}")
        yield
        self._write(f"*%{self.lf}")

    def _write(self, value: str) -> None:
        self.output.write(value)

    def on_ab_close(self, node: ABclose) -> None:  # noqa: ARG002
        """Handle `ABclose` node."""
        with self._extended_command("AB"):
            pass

    def on_ab_open(self, node: ABopen) -> None:
        """Handle `ABopen` node."""
        with self._extended_command("AB"):
            self._write(node.aperture_identifier)

    def on_adc(self, node: ADC) -> None:
        """Handle `AD` circle node."""
        with self._extended_command(f"AD{node.aperture_identifier}C,"):
            self._write(self._fmt_double(node.diameter))

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")

    def on_adr(self, node: ADR) -> None:
        """Handle `AD` rectangle node."""
        with self._extended_command(f"AD{node.aperture_identifier}R,"):
            self._write(self._fmt_double(node.width))
            self._write(f"X{self._fmt_double(node.height)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")

    def on_ado(self, node: ADO) -> None:
        """Handle `AD` obround node."""
        with self._extended_command(f"AD{node.aperture_identifier}O,"):
            self._write(self._fmt_double(node.width))
            self._write(f"X{self._fmt_double(node.height)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")

    def on_adp(self, node: ADP) -> None:
        """Handle `AD` polygon node."""
        with self._extended_command(f"AD{node.aperture_identifier}P,"):
            self._write(self._fmt_double(node.outer_diameter))
            self._write(f"X{node.vertices}")

            if node.rotation is not None:
                self._write(f"X{self._fmt_double(node.rotation)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")

    def on_ad_macro(self, node: ADmacro) -> None:
        """Handle `AD` macro node."""
        with self._extended_command(f"AD{node.aperture_identifier}{node.name}"):
            if node.params is not None:
                first, *rest = node.params
                self._write(f",{first}")
                for param in rest:
                    self._write(f"X{param}")

    def on_am_close(self, node: AMclose) -> None:
        """Handle `AMclose` node."""
        super().on_am_close(node)
        if self.macro_end_in_new_line:
            self._write(f"{self.lf}")
        self._write(f"%{self.lf}")

    def on_am_open(self, node: AMopen) -> None:
        """Handle `AMopen` node."""
        super().on_am_open(node)
        self._write(f"%AM{node.name}*")

    def on_sr_close(self, node: SRclose) -> None:  # noqa: ARG002
        """Handle `SRclose` node."""
        with self._extended_command("SR"):
            pass

    def on_sr_open(self, node: SRopen) -> None:
        """Handle `SRopen` node."""
        with self._extended_command("SR"):
            if node.x is not None:
                self._write(f"X{node.x}")

            if node.x is not None:
                self._write(f"Y{node.y}")

            if node.x is not None:
                self._write(f"I{node.i}")

            if node.x is not None:
                self._write(f"J{node.j}")

    # Attribute

    def on_ta_user_name(self, node: TA_UserName) -> None:
        """Handle `TA_UserName` node."""
        with self._extended_command(f"TA{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

    def on_ta_aper_function(self, node: TA_AperFunction) -> None:
        """Handle `TA_AperFunction` node."""
        with self._extended_command("TA.AperFunction"):
            if node.function is not None:
                self._write(",")
                self._write(node.function.value)

            for field in node.fields:
                self._write(",")
                self._write(field)

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> None:
        """Handle `TA_DrillTolerance` node."""
        with self._extended_command("TA.DrillTolerance"):
            if node.plus_tolerance is not None:
                self._write(",")
                self._write(self._fmt_double(node.plus_tolerance))

            if node.minus_tolerance is not None:
                self._write(",")
                self._write(self._fmt_double(node.minus_tolerance))

    def on_ta_flash_text(self, node: TA_FlashText) -> None:
        """Handle `TA_FlashText` node."""
        with self._extended_command("TA.FlashText"):
            self._write(",")
            self._write(node.string)

            self._write(",")
            self._write(node.mode)

            self._write(",")
            self._write(node.mirroring)

            if len(node.comments) == 0:
                if node.font is not None:
                    self._write(",")
                    self._write(node.font)

                if node.size is not None:
                    self._write(",")
                    self._write(node.size)

                for comment in node.comments:
                    self._write(",")
                    self._write(comment)
            else:
                self._write(",")
                if node.font is not None:
                    self._write(node.font)

                self._write(",")
                if node.size is not None:
                    self._write(node.size)

                for comment in node.comments:
                    self._write(",")
                    self._write(comment)

    def on_td(self, node: TD) -> None:
        """Handle `TD` node."""
        with self._extended_command("TD"):
            if node.name is not None:
                self._write(node.name)

    def on_tf_user_name(self, node: TF_UserName) -> None:
        """Handle `TF_UserName` node."""
        with self._extended_command(f"TF{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

    def on_tf_part(self, node: TF_Part) -> None:
        """Handle `TF_Part` node."""
        with self._extended_command("TF.Part,"):
            self._write(node.part.value)
            if len(node.fields) != 0:
                for field in node.fields:
                    self._write(",")
                    self._write(field)

    def on_tf_file_function(self, node: TF_FileFunction) -> None:
        """Handle `TF_FileFunction` node."""
        with self._extended_command("TF.FileFunction,"):
            self._write(node.file_function.value)
            if len(node.fields) != 0:
                for field in node.fields:
                    self._write(",")
                    self._write(field)

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> None:
        """Handle `TF_FilePolarity` node."""
        with self._extended_command("TF.FilePolarity,"):
            self._write(node.polarity)

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> None:
        """Handle `TF_SameCoordinates` node."""
        with self._extended_command("TF.SameCoordinates"):
            if node.identifier is not None:
                self._write(",")
                self._write(node.identifier)

    def on_tf_creation_date(self, node: TF_CreationDate) -> None:
        """Handle `TF_CreationDate` node."""
        with self._extended_command("TF.CreationDate"):
            if node.creation_date is not None:
                self._write(",")
                self._write(node.creation_date.isoformat())

    def on_tf_generation_software(self, node: TF_GenerationSoftware) -> None:
        """Handle `TF_GenerationSoftware` node."""
        with self._extended_command("TF.GenerationSoftware"):
            self._write(",")
            if node.vendor is not None:
                self._write(node.vendor)

            self._write(",")
            if node.application is not None:
                self._write(node.application)

            self._write(",")
            if node.version is not None:
                self._write(node.version)

    def on_tf_project_id(self, node: TF_ProjectId) -> None:
        """Handle `TF_ProjectId` node."""
        with self._extended_command("TF.ProjectId"):
            self._write(",")
            if node.name is not None:
                self._write(node.name)

            self._write(",")
            if node.guid is not None:
                self._write(node.guid)

            self._write(",")
            if node.revision is not None:
                self._write(node.revision)

    def on_tf_md5(self, node: TF_MD5) -> None:
        """Handle `TF_MD5` node."""
        with self._extended_command("TF.MD5"):
            self._write(",")
            self._write(node.md5)

    def on_to_user_name(self, node: TO_UserName) -> None:
        """Handle `TO_UserName` node."""
        with self._extended_command(f"TO{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

    def on_to_n(self, node: TO_N) -> None:
        """Handle `TO_N` node."""
        with self._extended_command("TO.N"):
            for field in node.net_names:
                self._write(",")
                self._write(field)

    def on_to_p(self, node: TO_P) -> None:
        """Handle `TO_P` node`."""
        with self._extended_command("TO.P"):
            self._write(",")
            self._write(node.refdes)
            self._write(",")
            self._write(node.number)
            if node.function is not None:
                self._write(",")
                self._write(node.function)

    def on_to_c(self, node: TO_C) -> None:
        """Handle `TO_C` node."""
        with self._extended_command("TO.C"):
            self._write(",")
            self._write(node.refdes)

    def on_to_crot(self, node: TO_CRot) -> None:
        """Handle `TO_CRot` node."""
        with self._extended_command("TO.CRot"):
            self._write(",")
            self._write(self._fmt_double(node.angle))

    def on_to_cmfr(self, node: TO_CMfr) -> None:
        """Handle `TO_CMfr` node."""
        with self._extended_command("TO.CMfr"):
            self._write(",")
            self._write(node.manufacturer)

    def on_to_cmnp(self, node: TO_CMNP) -> None:
        """Handle `TO_CMNP` node."""
        with self._extended_command("TO.CMPN"):
            self._write(",")
            self._write(node.part_number)

    def on_to_cval(self, node: TO_CVal) -> None:
        """Handle `TO_CVal` node."""
        with self._extended_command("TO.CVal"):
            self._write(",")
            self._write(node.value)

    def on_to_cmnt(self, node: TO_CMnt) -> None:
        """Handle `TO_CVal` node."""
        with self._extended_command("TO.CMnt"):
            self._write(",")
            self._write(node.mount.value)

    def on_to_cftp(self, node: TO_CFtp) -> None:
        """Handle `TO_Cftp` node."""
        with self._extended_command("TO.CFtp"):
            self._write(",")
            self._write(node.footprint)

    def on_to_cpgn(self, node: TO_CPgN) -> None:
        """Handle `TO_CPgN` node."""
        with self._extended_command("TO.CPgN"):
            self._write(",")
            self._write(node.name)

    def on_to_cpgd(self, node: TO_CPgD) -> None:
        """Handle `TO_CPgD` node."""
        with self._extended_command("TO.CPgD"):
            self._write(",")
            self._write(node.description)

    def on_to_chgt(self, node: TO_CHgt) -> None:
        """Handle `TO_CHgt` node."""
        with self._extended_command("TO.CHgt"):
            self._write(",")
            self._write(self._fmt_double(node.height))

    def on_to_clbn(self, node: TO_CLbN) -> None:
        """Handle `TO_CLbN` node."""
        with self._extended_command("TO.CLbn"):
            self._write(",")
            self._write(node.name)

    def on_to_clbd(self, node: TO_CLbD) -> None:
        """Handle `TO_CLbD` node."""
        with self._extended_command("TO.CLbD"):
            self._write(",")
            self._write(node.description)

    def on_to_csup(self, node: TO_CSup) -> None:
        """Handle `TO_CSup` node."""
        with self._extended_command("TO.CSup"):
            self._write(",")
            self._write(node.supplier)
            self._write(",")
            self._write(node.supplier_part)
            for field in node.other_suppliers:
                self._write(",")
                self._write(field)

    # D codes

    def on_d01(self, node: D01) -> None:
        """Handle `D01` node."""
        super().on_d01(node)
        with self._command("D01"):
            pass

    def on_d02(self, node: D02) -> None:
        """Handle `D02` node."""
        super().on_d02(node)
        with self._command("D02"):
            pass

    def on_d03(self, node: D03) -> None:
        """Handle `D03` node."""
        super().on_d03(node)
        with self._command("D03"):
            pass

    def on_dnn(self, node: Dnn) -> None:
        """Handle `Dnn` node."""
        with self._command(node.value):
            pass

    # G codes

    def on_g01(self, node: G01) -> None:  # noqa: ARG002
        """Handle `G01` node."""
        self._write("G01*\n")

    def on_g02(self, node: G02) -> None:  # noqa: ARG002
        """Handle `G02` node."""
        self._write("G02*\n")

    def on_g03(self, node: G03) -> None:  # noqa: ARG002
        """Handle `G03` node."""
        self._write("G03*\n")

    def on_g04(self, node: G04) -> None:
        """Handle `G04` node."""
        self._write(f"G04{node.string or ''}*\n")

    def on_g36(self, node: G36) -> None:  # noqa: ARG002
        """Handle `G36` node."""
        self._write("G36*\n")

    def on_g37(self, node: G37) -> None:  # noqa: ARG002
        """Handle `G37` node."""
        self._write("G37*\n")

    def on_g54(self, node: G54) -> None:
        """Handle `G54` node."""
        self._write("G54")
        super().on_g54(node)

    def on_g55(self, node: G55) -> None:
        """Handle `G55` node."""
        self._write("G55")
        super().on_g55(node)

    def on_g70(self, node: G70) -> None:  # noqa: ARG002
        """Handle `G70` node."""
        self._write("G70*\n")

    def on_g71(self, node: G71) -> None:  # noqa: ARG002
        """Handle `G71` node."""
        self._write("G71*\n")

    def on_g74(self, node: G74) -> None:  # noqa: ARG002
        """Handle `G74` node."""
        self._write("G74*\n")

    def on_g75(self, node: G75) -> None:  # noqa: ARG002
        """Handle `G75` node."""
        self._write("G75*\n")

    def on_g90(self, node: G90) -> None:  # noqa: ARG002
        """Handle `G90` node."""
        self._write("G90*\n")

    def on_g91(self, node: G91) -> None:  # noqa: ARG002
        """Handle `G91` node."""
        self._write("G91*\n")

    # Load

    def on_lm(self, node: LM) -> None:
        """Handle `LM` node."""
        super().on_lm(node)

    def on_ln(self, node: LN) -> None:
        """Handle `LN` node."""
        super().on_ln(node)

    def on_lp(self, node: LP) -> None:
        """Handle `LP` node."""
        super().on_lp(node)

    def on_lr(self, node: LR) -> None:
        """Handle `LR` node."""
        super().on_lr(node)

    def on_ls(self, node: LS) -> None:
        """Handle `LS` node."""
        super().on_ls(node)

    # M Codes

    def on_m00(self, node: M00) -> None:  # noqa: ARG002
        """Handle `M00` node."""
        with self._command("M00"):
            pass

    def on_m01(self, node: M01) -> None:  # noqa: ARG002
        """Handle `M01` node."""
        with self._command("M01"):
            pass

    def on_m02(self, node: M02) -> None:  # noqa: ARG002
        """Handle `M02` node."""
        with self._command("M02"):
            pass

    # Math

    # Math :: Operators :: Binary
    def on_add(self, node: Add) -> None:
        """Handle `Add` node."""
        self._write("(")
        for i, operand in enumerate(node.operands):
            operand.visit(self)
            if i < len(node.operands) - 1:
                self._write("+")
        self._write(")")

    def on_div(self, node: Div) -> None:
        """Handle `Div` node."""
        self._write("(")
        for i, operand in enumerate(node.operands):
            operand.visit(self)
            if i < len(node.operands) - 1:
                self._write("/")
        self._write(")")

    def on_mul(self, node: Mul) -> None:
        """Handle `Mul` node."""
        self._write("(")
        for i, operand in enumerate(node.operands):
            operand.visit(self)
            if i < len(node.operands) - 1:
                self._write("x")
        self._write(")")

    def on_sub(self, node: Sub) -> None:
        """Handle `Sub` node."""
        self._write("(")
        for i, operand in enumerate(node.operands):
            operand.visit(self)
            if i < len(node.operands) - 1:
                self._write("-")
        self._write(")")

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> None:
        """Handle `Neg` node."""
        self._write("-")
        node.operand.visit(self)

    def on_pos(self, node: Pos) -> None:
        """Handle `Pos` node."""
        self._write("+")
        node.operand.visit(self)

    def on_assignment(self, node: Assignment) -> None:
        """Handle `Assignment` node."""
        self._write(self._macro_primitive_lf)
        node.variable.visit(self)
        self._write("=")
        node.expression.visit(self)
        self._write("*")

    def on_constant(self, node: Constant) -> None:
        """Handle `Constant` node."""
        self._write(self._fmt_double(node.constant))

    def on_point(self, node: Point) -> None:
        """Handle `Point` node."""
        node.x.visit(self)
        self._write(",")
        node.y.visit(self)

    def on_variable(self, node: Variable) -> None:
        """Handle `Variable` node."""
        self._write(node.variable)

    # Other

    def on_coordinate_x(self, node: CoordinateX) -> None:
        """Handle `Coordinate` node."""
        self._write(f"X{node.value}")

    def on_coordinate_y(self, node: CoordinateY) -> None:
        """Handle `Coordinate` node."""
        self._write(f"Y{node.value}")

    def on_coordinate_i(self, node: CoordinateI) -> None:
        """Handle `Coordinate` node."""
        self._write(f"I{node.value}")

    def on_coordinate_j(self, node: CoordinateJ) -> None:
        """Handle `Coordinate` node."""
        self._write(f"J{node.value}")

    # Primitives

    def on_code_0(self, node: Code0) -> None:
        """Handle `Code0` node."""
        self._write(f"{self._macro_primitive_lf}0{node.string}*")

    def on_code_1(self, node: Code1) -> None:
        """Handle `Code1` node."""
        self._write(f"{self._macro_primitive_lf}1,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.diameter.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_y.visit(self)
        if node.rotation is not None:
            self._write(f",{self._macro_param_lf}")
            node.rotation.visit(self)
        self._write("*")

    @cached_property
    def _macro_primitive_lf(self) -> str:
        if self.macro_split_mode == self.MacroSplitMode.NONE or self.strip_whitespace:
            return ""

        if self.macro_split_mode in (
            self.MacroSplitMode.PRIMITIVES,
            self.MacroSplitMode.PARAMETERS,
        ):
            return self.lf + self.macro_body_indent

        msg = f"Unsupported macro split mode: {self.macro_split_mode}"
        raise NotImplementedError(msg)

    @cached_property
    def _macro_param_lf(self) -> str:
        if (
            self.macro_split_mode
            in (self.MacroSplitMode.NONE, self.MacroSplitMode.PRIMITIVES)
            or self.strip_whitespace
        ):
            return ""

        if self.macro_split_mode == self.MacroSplitMode.PARAMETERS:
            return self.lf + self.macro_param_indent + self.macro_body_indent

        msg = f"Unsupported macro split mode: {self.macro_split_mode}"
        raise NotImplementedError(msg)

    def on_code_2(self, node: Code2) -> None:
        """Handle `Code2` node."""
        self._write(f"{self._macro_primitive_lf}2,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.width.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.end_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.end_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_4(self, node: Code4) -> None:
        """Handle `Code4` node."""
        self._write(f"{self._macro_primitive_lf}4,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.number_of_points.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_y.visit(self)
        for point in node.points:
            self._write(f",{self._macro_param_lf}")
            point.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_5(self, node: Code5) -> None:
        """Handle `Code5` node."""
        self._write(f"{self._macro_primitive_lf}5,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.number_of_vertices.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.diameter.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_6(self, node: Code6) -> None:
        """Handle `Code6` node."""
        self._write(f"{self._macro_primitive_lf}6,{self._macro_param_lf}")
        node.center_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.outer_diameter.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.ring_thickness.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.gap_between_rings.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.max_ring_count.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.crosshair_thickness.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.crosshair_length.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_7(self, node: Code7) -> None:
        """Handle `Code7` node."""
        self._write(f"{self._macro_primitive_lf}7,{self._macro_param_lf}")
        node.center_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.outer_diameter.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.inner_diameter.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.gap_thickness.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_20(self, node: Code20) -> None:
        """Handle `Code20` node."""
        self._write(f"{self._macro_primitive_lf}20,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.width.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.start_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.end_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.end_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_21(self, node: Code21) -> None:
        """Handle `Code21` node."""
        self._write(f"{self._macro_primitive_lf}21,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.width.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.height.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_x.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.center_y.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    def on_code_22(self, node: Code22) -> None:
        """Handle `Code22` node."""
        self._write(f"{self._macro_primitive_lf}22,{self._macro_param_lf}")
        node.exposure.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.width.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.height.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.x_lower_left.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.y_lower_left.visit(self)
        self._write(f",{self._macro_param_lf}")
        node.rotation.visit(self)
        self._write("*")

    # Properties

    def on_as(self, node: AS) -> None:
        """Handle `AS` node."""
        with self._extended_command("AS"):
            self._write(node.correspondence.value)

    def on_fs(self, node: FS) -> None:
        """Handle `FS` node."""
        with self._extended_command("FS"):
            self._write(node.zeros)
            self._write(node.coordinate_mode)
            self._write(f"X{node.x_integral}{node.x_decimal}")
            self._write(f"Y{node.y_integral}{node.y_decimal}")

    def on_in(self, node: IN) -> None:
        """Handle `IN` node."""
        with self._extended_command("IN"):
            self._write(node.name)

    def on_ip(self, node: IP) -> None:
        """Handle `IP` node."""
        with self._extended_command("IP"):
            self._write(node.polarity)

    def on_ir(self, node: IR) -> None:
        """Handle `IR` node."""
        with self._extended_command("IR"):
            self._write(self._fmt_double(node.rotation_degrees))

    def on_mi(self, node: MI) -> None:
        """Handle `MI` node."""
        with self._extended_command("MI"):
            self._write(f"A{node.a_mirroring}")
            self._write(f"B{node.b_mirroring}")

    def on_mo(self, node: MO) -> None:
        """Handle `MO` node."""
        with self._extended_command("MO"):
            self._write(node.mode.value)

    def on_of(self, node: OF) -> None:
        """Handle `OF` node."""
        with self._extended_command("OF"):
            if node.a_offset is not None:
                self._write(f"A{node.a_offset}")
            if node.b_offset is not None:
                self._write(f"B{node.b_offset}")

    def on_sf(self, node: SF) -> None:
        """Handle `SF` node."""
        with self._extended_command("SF"):
            self._write("A")
            self._write(self._fmt_double(node.a_scale))
            self._write("B")
            self._write(self._fmt_double(node.b_scale))

    # Root node

    def on_file(self, node: File) -> None:
        """Handle `File` node."""
        super().on_file(node)
