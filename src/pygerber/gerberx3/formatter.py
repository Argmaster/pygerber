"""`pygerber.gerberx3.formatter` module contains implementation `Formatter` class
which implements configurable Gerber code formatting.
"""

from __future__ import annotations

from contextlib import contextmanager
from enum import Enum
from functools import wraps
from io import StringIO
from typing import (
    Callable,
    Generator,
    Literal,
    Optional,
    Type,
    TypeVar,
)

from pyparsing import cached_property
from typing_extensions import ParamSpec

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.nodes import (
    ADC,
    ADO,
    ADP,
    ADR,
    AS,
    D01,
    D02,
    D03,
    FS,
    G01,
    G02,
    G03,
    G04,
    G36,
    G37,
    G54,
    G55,
    G70,
    G71,
    G74,
    G75,
    G90,
    G91,
    IN,
    IP,
    IR,
    LM,
    LN,
    LP,
    LR,
    LS,
    M00,
    M01,
    M02,
    MI,
    MO,
    OF,
    SF,
    TD,
    TF_MD5,
    TO_C,
    TO_CMNP,
    TO_N,
    TO_P,
    ABclose,
    ABopen,
    Add,
    ADmacro,
    AMclose,
    AMopen,
    Assignment,
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
    Constant,
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
    Div,
    Dnn,
    Double,
    File,
    G,
    Mul,
    Neg,
    Node,
    Parenthesis,
    Point,
    Pos,
    SRclose,
    SRopen,
    Sub,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
    TF_CreationDate,
    TF_FileFunction,
    TF_FilePolarity,
    TF_GenerationSoftware,
    TF_Part,
    TF_ProjectId,
    TF_SameCoordinates,
    TF_UserName,
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
    Variable,
)


class FormatterError(Exception):
    """Formatter error."""


ParamT = ParamSpec("ParamT")
ReturnT = TypeVar("ReturnT")


def _increase_base_indent(
    variable_name: str,
) -> Callable[[Callable[ParamT, ReturnT]], Callable[ParamT, ReturnT]]:
    def _decorator(
        function: Callable[ParamT, ReturnT],
    ) -> Callable[ParamT, ReturnT]:
        @wraps(function)
        def _(*args: ParamT.args, **kwargs: ParamT.kwargs) -> ReturnT:
            self = args[0]
            assert isinstance(self, Formatter)

            self._base_indent += getattr(self, variable_name)

            return function(*args, **kwargs)

        return _

    return _decorator


def _decrease_base_indent(
    variable_name: str,
) -> Callable[[Callable[ParamT, ReturnT]], Callable[ParamT, ReturnT]]:
    def _decorator(
        function: Callable[ParamT, ReturnT],
    ) -> Callable[ParamT, ReturnT]:
        @wraps(function)
        def _(*args: ParamT.args, **kwargs: ParamT.kwargs) -> ReturnT:
            self = args[0]
            assert isinstance(self, Formatter)

            indent_delta = getattr(self, variable_name)
            if self._base_indent.endswith(indent_delta):
                self._base_indent = self._base_indent[: -len(indent_delta)]

            return function(*args, **kwargs)

        return _

    return _decorator


def _decorator_insert_base_indent(
    function: Callable[ParamT, ReturnT],
) -> Callable[ParamT, ReturnT]:
    @wraps(function)
    def _(*args: ParamT.args, **kwargs: ParamT.kwargs) -> ReturnT:
        self = args[0]
        assert isinstance(self, Formatter)
        self._insert_base_indent()
        return function(*args, **kwargs)

    return _


def _insert_var(
    variable_name_or_getter: str | Callable[[Formatter], str],
) -> Callable[[Callable[ParamT, ReturnT]], Callable[ParamT, ReturnT]]:
    def _decorator(
        function: Callable[ParamT, ReturnT],
    ) -> Callable[ParamT, ReturnT]:
        @wraps(function)
        def _(*args: ParamT.args, **kwargs: ParamT.kwargs) -> ReturnT:
            self = args[0]
            assert isinstance(self, Formatter)
            if isinstance(variable_name_or_getter, str):
                self._write(getattr(self, variable_name_or_getter))
            else:
                self._write(variable_name_or_getter(self))

            return function(*args, **kwargs)

        return _

    return _decorator


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
        macro_body_indent: str | int = 0,
        macro_param_indent: str | int = 0,
        macro_split_mode: MacroSplitMode = MacroSplitMode.PRIMITIVES,
        macro_end_in_new_line: bool = False,
        block_aperture_body_indent: str | int = 0,
        step_and_repeat_body_indent: str | int = 0,
        float_decimal_places: int = -1,
        float_trim_trailing_zeros: bool = True,
        d01_indent: int | str = 0,
        d02_indent: int | str = 0,
        d03_indent: int | str = 0,
        line_end: Literal["\n", "\r\n"] = "\n",
        empty_line_before_polarity_switch: bool = False,
        keep_non_standalone_codes: bool = True,
        remove_g54: bool = False,
        remove_g55: bool = False,
        explicit_parenthesis: bool = False,
        strip_whitespace: bool = False,
    ) -> None:
        r"""Initialize Formatter instance.

        Parameters
        ----------
        indent_character: Literal[" ", "\t"], optional
            Character used for indentation, by default " "
        macro_body_indent : str | int, optional
            Indentation of macro body, by default 0
        macro_param_indent: str | int, optional
            Indentation of macro parameters, by default 0
            This indentation is added on top of macro body indentation.
            This has effect only when `macro_split_mode` is `PARAMETERS`.
        macro_split_mode : `Formatter.MacroSplitMode`, optional
            Changes how macro definitions are formatted, by default `NONE`
            When `NONE` is selected, macro will be formatted as a single line.
            ```gerber
            %AMDonut*1,1,$1,$2,$3*$4=$1x0.75*1,0,$4,$2,$3*%
            ```
            When `PRIMITIVES` is selected, macro will be formatted with each primitive
            on a new line.
            ```gerber
            %AMDonut*
            1,1,$1,$2,$3*
            $4=$1x0.75*
            1,0,$4,$2,$3*%
            ```
            When `PARAMETERS` is selected, macro will be formatted with each primitive
            on a new line and each parameter of a primitive on a new line.
            ```gerber
            %AMDonut*
            1,
            1,
            $1,
            $2,
            $3*
            $4=$1x0.75*
            1,
            0,
            $4,
            $2,
            $3*%
            ```
            Use `macro_body_indent` and `macro_param_indent` to control indentation.
        macro_end_in_new_line: bool, optional
            Place % sign which marks the end of macro in new line, by default False
        block_aperture_body_indent : str | int, optional
            Indentation of block aperture definition body, by default 0
            This indentations stacks for nested block apertures.
        step_and_repeat_body_indent : str | int, optional
            Indentation of step and repeat definition body, by default 0
            This indentations stacks for nested step and repeat blocks.
        float_decimal_places : int, optional
            Limit number of decimal places shown for float values, by default -1
            Negative values are interpreted as no limit.
        float_trim_trailing_zeros : bool, optional
            Remove trailing zeros from floats, by default True
            When this is enabled, after floating point number is formatted with respect
            to `float_decimal_places`, trailing zeros are removed. If all zeros after
            decimal point are removed, decimal point is also removed.
        d01_indent : str | int, optional
            Custom indentation of D01 command, by default 0
        d02_indent : str | int, optional
            Custom indentation of D02 command, by default 0
        d03_indent : str | int, optional
            Custom indentation of D03 command, by default 0
        line_end : Literal["\n", "\r\n"], optional
            Line ending character, Unix or Windows style, by default "\n" (Unix style)
            If `strip_whitespace` is enabled, no line end will be used.
        empty_line_before_polarity_switch : bool, optional
            Add empty line before polarity switch, by default False
            This enhances visibility of sequences of commands with different
            polarities.
        keep_non_standalone_codes: bool, optional
            Keep non-standalone codes in the output, by default True
            If this option is disabled, codes that are not standalone, ie. `G70D02*`
            will be divided into two separate commands, `G70*` and `D02*`, otherwise
            they will be kept as is.
        remove_g54: bool, optional
            Remove G54 code from output, by default False
            G54 code has no effect on the output, it was used in legacy files to
            prefix select aperture command.
        remove_g55: bool, optional
            Remove G55 code from output, by default False
            G55 code has no effect on the output, it was used in legacy files to
            prefix flash command.
        explicit_parenthesis: bool, optional
            Add explicit parenthesis around all mathematical
            expressions within macro, by default False
            When false, original parenthesis are kept.
        strip_whitespace : bool, optional
            Remove all semantically insignificant whitespace, by default False

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

        if isinstance(block_aperture_body_indent, int):
            block_aperture_body_indent = indent_character * block_aperture_body_indent
        self.block_aperture_body_indent = block_aperture_body_indent

        if isinstance(step_and_repeat_body_indent, int):
            step_and_repeat_body_indent = indent_character * step_and_repeat_body_indent
        self.step_and_repeat_body_indent = step_and_repeat_body_indent

        self.float_decimal_places = float_decimal_places

        self.float_trim_trailing_zeros = float_trim_trailing_zeros

        if isinstance(d01_indent, int):
            d01_indent = indent_character * d01_indent
        self.d01_indent = d01_indent

        if isinstance(d02_indent, int):
            d02_indent = indent_character * d02_indent
        self.d02_indent = d02_indent

        if isinstance(d03_indent, int):
            d03_indent = indent_character * d03_indent
        self.d03_indent = d03_indent

        self.lf = line_end
        self.empty_line_before_polarity_switch = (
            self.lf if empty_line_before_polarity_switch else ""
        )
        self.keep_non_standalone_codes = keep_non_standalone_codes
        self.remove_g54 = remove_g54
        self.remove_g55 = remove_g55
        self.explicit_parenthesis = explicit_parenthesis
        self.strip_whitespace = strip_whitespace

        if self.strip_whitespace:
            self.lf = ""  # type: ignore[assignment]
            self.indent_character = ""  # type: ignore[assignment]
            self.macro_body_indent = ""
            self.macro_param_indent = ""
            self.block_aperture_body_indent = ""
            self.step_and_repeat_body_indent = ""
            self.d01_indent = ""
            self.d02_indent = ""
            self.d03_indent = ""
            self.empty_line_before_polarity_switch = ""

        self._output: Optional[StringIO] = None
        self._base_indent: str = ""

    def format(self, source: File, output: StringIO) -> None:
        """Format Gerber AST according to rules specified in Formatter constructor."""
        self._output = output
        try:
            self.on_file(source)
        finally:
            self._output = None
            self._base_indent = ""

    def formats(self, source: File) -> str:
        """Format Gerber AST according to rules specified in Formatter constructor."""
        out = StringIO()
        self.format(source, out)
        return out.getvalue()

    def format_node(self, node: Node, output: StringIO) -> None:
        """Format single node according to rules specified in Formatter constructor."""
        self._output = output
        try:
            node.visit(self)
        finally:
            self._output = None
            self._base_indent = ""

    def formats_node(self, node: File) -> str:
        """Format single node according to rules specified in Formatter constructor."""
        out = StringIO()
        self.format_node(node, out)
        return out.getvalue()

    @property
    def output(self) -> StringIO:
        """Get output buffer."""
        if self._output is None:
            msg = "Output buffer is not set."
            raise FormatterError(msg)

        return self._output

    def _fmt_double(self, value: Double) -> str:
        if self.float_decimal_places < 0:
            return str(value)
        double = f"{value:.{self.float_decimal_places}f}"
        if self.float_trim_trailing_zeros:
            return double.rstrip("0").rstrip(".")
        return double

    def _insert_base_indent(self) -> None:
        self._write(self._base_indent)

    def _insert_extra_indent(self, value: str) -> None:
        self._write(value)

    @contextmanager
    def _command(
        self, cmd: str, *, asterisk: bool = True, lf: bool = True
    ) -> Generator[None, None, None]:
        self._write(cmd)
        yield
        if asterisk:
            self._write("*")
        if lf:
            self._write(self.lf)

    @contextmanager
    def _extended_command(self, cmd: str) -> Generator[None, None, None]:
        self._write(f"%{cmd}")
        yield
        self._write(f"*%{self.lf}")

    def _write(self, value: str) -> None:
        self.output.write(value)

    @_decrease_base_indent("block_aperture_body_indent")
    @_decorator_insert_base_indent
    def on_ab_close(self, node: ABclose) -> ABclose:
        """Handle `ABclose` node."""
        with self._extended_command("AB"):
            pass
        return node

    @_decorator_insert_base_indent
    @_increase_base_indent("block_aperture_body_indent")
    def on_ab_open(self, node: ABopen) -> ABopen:
        """Handle `ABopen` node."""
        with self._extended_command("AB"):
            self._write(node.aperture_id)
        return node

    @_decorator_insert_base_indent
    def on_adc(self, node: ADC) -> ADC:
        """Handle `AD` circle node."""
        with self._extended_command(f"AD{node.aperture_id}C,"):
            self._write(self._fmt_double(node.diameter))

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")
        return node

    @_decorator_insert_base_indent
    def on_adr(self, node: ADR) -> ADR:
        """Handle `AD` rectangle node."""
        with self._extended_command(f"AD{node.aperture_id}R,"):
            self._write(self._fmt_double(node.width))
            self._write(f"X{self._fmt_double(node.height)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")
        return node

    @_decorator_insert_base_indent
    def on_ado(self, node: ADO) -> ADO:
        """Handle `AD` obround node."""
        with self._extended_command(f"AD{node.aperture_id}O,"):
            self._write(self._fmt_double(node.width))
            self._write(f"X{self._fmt_double(node.height)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")
        return node

    @_decorator_insert_base_indent
    def on_adp(self, node: ADP) -> ADP:
        """Handle `AD` polygon node."""
        with self._extended_command(f"AD{node.aperture_id}P,"):
            self._write(self._fmt_double(node.outer_diameter))
            self._write(f"X{node.vertices}")

            if node.rotation is not None:
                self._write(f"X{self._fmt_double(node.rotation)}")

            if node.hole_diameter is not None:
                self._write(f"X{self._fmt_double(node.hole_diameter)}")
        return node

    @_decorator_insert_base_indent
    def on_ad_macro(self, node: ADmacro) -> ADmacro:
        """Handle `AD` macro node."""
        with self._extended_command(f"AD{node.aperture_id}{node.name}"):
            if node.params is not None:
                first, *rest = node.params
                self._write(f",{first}")
                for param in rest:
                    self._write(f"X{param}")
        return node

    @_decorator_insert_base_indent
    def on_am_close(self, node: AMclose) -> AMclose:
        """Handle `AMclose` node."""
        super().on_am_close(node)
        if self.macro_end_in_new_line:
            self._write(f"{self.lf}")
        self._write(f"%{self.lf}")
        return node

    @_decorator_insert_base_indent
    def on_am_open(self, node: AMopen) -> AMopen:
        """Handle `AMopen` node."""
        super().on_am_open(node)
        self._write(f"%AM{node.name}*")
        return node

    @_decrease_base_indent("step_and_repeat_body_indent")
    @_decorator_insert_base_indent
    def on_sr_close(self, node: SRclose) -> SRclose:
        """Handle `SRclose` node."""
        with self._extended_command("SR"):
            pass
        return node

    @_decorator_insert_base_indent
    @_increase_base_indent("step_and_repeat_body_indent")
    def on_sr_open(self, node: SRopen) -> SRopen:
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

        return node

    # Attribute

    @_decorator_insert_base_indent
    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:
        """Handle `TA_UserName` node."""
        with self._extended_command(f"TA{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_ta_aper_function(self, node: TA_AperFunction) -> TA_AperFunction:
        """Handle `TA_AperFunction` node."""
        with self._extended_command("TA.AperFunction"):
            if node.function is not None:
                self._write(",")
                self._write(node.function.value)

            for field in node.fields:
                self._write(",")
                self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> TA_DrillTolerance:
        """Handle `TA_DrillTolerance` node."""
        with self._extended_command("TA.DrillTolerance"):
            if node.plus_tolerance is not None:
                self._write(",")
                self._write(self._fmt_double(node.plus_tolerance))

            if node.minus_tolerance is not None:
                self._write(",")
                self._write(self._fmt_double(node.minus_tolerance))

        return node

    @_decorator_insert_base_indent
    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:
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

        return node

    @_decorator_insert_base_indent
    def on_td(self, node: TD) -> TD:
        """Handle `TD` node."""
        with self._extended_command("TD"):
            if node.name is not None:
                self._write(node.name)

        return node

    @_decorator_insert_base_indent
    def on_tf_user_name(self, node: TF_UserName) -> TF_UserName:
        """Handle `TF_UserName` node."""
        with self._extended_command(f"TF{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_tf_part(self, node: TF_Part) -> TF_Part:
        """Handle `TF_Part` node."""
        with self._extended_command("TF.Part,"):
            self._write(node.part.value)
            if len(node.fields) != 0:
                for field in node.fields:
                    self._write(",")
                    self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_tf_file_function(self, node: TF_FileFunction) -> TF_FileFunction:
        """Handle `TF_FileFunction` node."""
        with self._extended_command("TF.FileFunction,"):
            self._write(node.file_function.value)
            if len(node.fields) != 0:
                for field in node.fields:
                    self._write(",")
                    self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_tf_file_polarity(self, node: TF_FilePolarity) -> TF_FilePolarity:
        """Handle `TF_FilePolarity` node."""
        with self._extended_command("TF.FilePolarity,"):
            self._write(node.polarity)

        return node

    @_decorator_insert_base_indent
    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> TF_SameCoordinates:
        """Handle `TF_SameCoordinates` node."""
        with self._extended_command("TF.SameCoordinates"):
            if node.identifier is not None:
                self._write(",")
                self._write(node.identifier)

        return node

    @_decorator_insert_base_indent
    def on_tf_creation_date(self, node: TF_CreationDate) -> TF_CreationDate:
        """Handle `TF_CreationDate` node."""
        with self._extended_command("TF.CreationDate"):
            if node.creation_date is not None:
                self._write(",")
                self._write(node.creation_date.isoformat())

        return node

    @_decorator_insert_base_indent
    def on_tf_generation_software(
        self, node: TF_GenerationSoftware
    ) -> TF_GenerationSoftware:
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

        return node

    @_decorator_insert_base_indent
    def on_tf_project_id(self, node: TF_ProjectId) -> TF_ProjectId:
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

        return node

    @_decorator_insert_base_indent
    def on_tf_md5(self, node: TF_MD5) -> TF_MD5:
        """Handle `TF_MD5` node."""
        with self._extended_command("TF.MD5"):
            self._write(",")
            self._write(node.md5)

        return node

    @_decorator_insert_base_indent
    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:
        """Handle `TO_UserName` node."""
        with self._extended_command(f"TO{node.user_name}"):
            for field in node.fields:
                self._write(",")
                self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_to_n(self, node: TO_N) -> TO_N:
        """Handle `TO_N` node."""
        with self._extended_command("TO.N"):
            for field in node.net_names:
                self._write(",")
                self._write(field)

        return node

    @_decorator_insert_base_indent
    def on_to_p(self, node: TO_P) -> TO_P:
        """Handle `TO_P` node`."""
        with self._extended_command("TO.P"):
            self._write(",")
            self._write(node.refdes)
            self._write(",")
            self._write(node.number)
            if node.function is not None:
                self._write(",")
                self._write(node.function)

        return node

    @_decorator_insert_base_indent
    def on_to_c(self, node: TO_C) -> TO_C:
        """Handle `TO_C` node."""
        with self._extended_command("TO.C"):
            self._write(",")
            self._write(node.refdes)

        return node

    @_decorator_insert_base_indent
    def on_to_crot(self, node: TO_CRot) -> TO_CRot:
        """Handle `TO_CRot` node."""
        with self._extended_command("TO.CRot"):
            self._write(",")
            self._write(self._fmt_double(node.angle))

        return node

    @_decorator_insert_base_indent
    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:
        """Handle `TO_CMfr` node."""
        with self._extended_command("TO.CMfr"):
            self._write(",")
            self._write(node.manufacturer)

        return node

    @_decorator_insert_base_indent
    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:
        """Handle `TO_CMNP` node."""
        with self._extended_command("TO.CMPN"):
            self._write(",")
            self._write(node.part_number)

        return node

    @_decorator_insert_base_indent
    def on_to_cval(self, node: TO_CVal) -> TO_CVal:
        """Handle `TO_CVal` node."""
        with self._extended_command("TO.CVal"):
            self._write(",")
            self._write(node.value)

        return node

    @_decorator_insert_base_indent
    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:
        """Handle `TO_CVal` node."""
        with self._extended_command("TO.CMnt"):
            self._write(",")
            self._write(node.mount.value)

        return node

    @_decorator_insert_base_indent
    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:
        """Handle `TO_Cftp` node."""
        with self._extended_command("TO.CFtp"):
            self._write(",")
            self._write(node.footprint)

        return node

    @_decorator_insert_base_indent
    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:
        """Handle `TO_CPgN` node."""
        with self._extended_command("TO.CPgN"):
            self._write(",")
            self._write(node.name)

        return node

    @_decorator_insert_base_indent
    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:
        """Handle `TO_CPgD` node."""
        with self._extended_command("TO.CPgD"):
            self._write(",")
            self._write(node.description)

        return node

    @_decorator_insert_base_indent
    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:
        """Handle `TO_CHgt` node."""
        with self._extended_command("TO.CHgt"):
            self._write(",")
            self._write(self._fmt_double(node.height))

        return node

    @_decorator_insert_base_indent
    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:
        """Handle `TO_CLbN` node."""
        with self._extended_command("TO.CLbn"):
            self._write(",")
            self._write(node.name)

        return node

    @_decorator_insert_base_indent
    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:
        """Handle `TO_CLbD` node."""
        with self._extended_command("TO.CLbD"):
            self._write(",")
            self._write(node.description)

        return node

    @_decorator_insert_base_indent
    def on_to_csup(self, node: TO_CSup) -> TO_CSup:
        """Handle `TO_CSup` node."""
        with self._extended_command("TO.CSup"):
            self._write(",")
            self._write(node.supplier)
            self._write(",")
            self._write(node.supplier_part)
            for field in node.other_suppliers:
                self._write(",")
                self._write(field)

        return node

    # D codes

    def on_d01(self, node: D01) -> D01:
        """Handle `D01` node."""
        if node.is_standalone or not self.keep_non_standalone_codes:
            self._insert_base_indent()
            self._insert_extra_indent(self.d01_indent)

        super().on_d01(node)
        with self._command("D01"):
            pass

        return node

    def on_d02(self, node: D02) -> D02:
        """Handle `D02` node."""
        if node.is_standalone or not self.keep_non_standalone_codes:
            self._insert_base_indent()
            self._insert_extra_indent(self.d02_indent)

        super().on_d02(node)
        with self._command("D02"):
            pass

        return node

    def on_d03(self, node: D03) -> D03:
        """Handle `D03` node."""
        if node.is_standalone or not self.keep_non_standalone_codes:
            self._insert_base_indent()
            self._insert_extra_indent(self.d03_indent)

        super().on_d03(node)
        with self._command("D03"):
            pass

        return node

    def on_dnn(self, node: Dnn) -> Dnn:
        """Handle `Dnn` node."""
        if node.is_standalone or not self.keep_non_standalone_codes:
            self._insert_base_indent()

        with self._command(node.aperture_id):
            pass

        return node

    # G codes

    def _handle_g(self, node: G, cls: Type[G]) -> None:
        if node.is_standalone or not self.keep_non_standalone_codes:
            with self._command(cls.__qualname__):
                pass
            return

        self._write(cls.__qualname__)

    @_decorator_insert_base_indent
    def on_g01(self, node: G01) -> G01:
        """Handle `G01` node."""
        self._handle_g(node, G01)
        return node

    @_decorator_insert_base_indent
    def on_g02(self, node: G02) -> G02:
        """Handle `G02` node."""
        self._handle_g(node, G02)
        return node

    @_decorator_insert_base_indent
    def on_g03(self, node: G03) -> G03:
        """Handle `G03` node."""
        self._handle_g(node, G03)
        return node

    @_decorator_insert_base_indent
    def on_g04(self, node: G04) -> G04:
        """Handle `G04` node."""
        with self._command(f"G04{node.string or ''}"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_g36(self, node: G36) -> G36:
        """Handle `G36` node."""
        self._handle_g(node, G36)
        return node

    @_decorator_insert_base_indent
    def on_g37(self, node: G37) -> G37:
        """Handle `G37` node."""
        self._handle_g(node, G37)
        return node

    @_decorator_insert_base_indent
    def on_g54(self, node: G54) -> G54:
        """Handle `G54` node."""
        if self.remove_g54:
            return node
        self._handle_g(node, G54)
        return node

    @_decorator_insert_base_indent
    def on_g55(self, node: G55) -> G55:
        """Handle `G55` node."""
        if self.remove_g55:
            return node
        self._handle_g(node, G55)
        return node

    @_decorator_insert_base_indent
    def on_g70(self, node: G70) -> G70:
        """Handle `G70` node."""
        self._handle_g(node, G70)
        return node

    @_decorator_insert_base_indent
    def on_g71(self, node: G71) -> G71:
        """Handle `G71` node."""
        self._handle_g(node, G71)
        return node

    @_decorator_insert_base_indent
    def on_g74(self, node: G74) -> G74:
        """Handle `G74` node."""
        self._handle_g(node, G74)
        return node

    @_decorator_insert_base_indent
    def on_g75(self, node: G75) -> G75:
        """Handle `G75` node."""
        self._handle_g(node, G75)
        return node

    @_decorator_insert_base_indent
    def on_g90(self, node: G90) -> G90:
        """Handle `G90` node."""
        self._handle_g(node, G90)
        return node

    @_decorator_insert_base_indent
    def on_g91(self, node: G91) -> G91:
        """Handle `G91` node."""
        self._handle_g(node, G91)
        return node

    # Load

    @_decorator_insert_base_indent
    def on_lm(self, node: LM) -> LM:
        """Handle `LM` node."""
        with self._extended_command(f"LM{node.mirroring.value}"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_ln(self, node: LN) -> LN:
        """Handle `LN` node."""
        with self._extended_command(f"LN{node.name}"):
            pass
        return node

    @_insert_var("empty_line_before_polarity_switch")
    @_decorator_insert_base_indent
    def on_lp(self, node: LP) -> LP:
        """Handle `LP` node."""
        with self._extended_command(f"LP{node.polarity.value}"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_lr(self, node: LR) -> LR:
        """Handle `LR` node."""
        with self._extended_command(f"LR{self._fmt_double(node.rotation)}"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_ls(self, node: LS) -> LS:
        """Handle `LS` node."""
        with self._extended_command(f"LS{self._fmt_double(node.scale)}"):
            pass
        return node

    # M Codes

    @_decorator_insert_base_indent
    def on_m00(self, node: M00) -> M00:
        """Handle `M00` node."""
        with self._command("M00"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_m01(self, node: M01) -> M01:
        """Handle `M01` node."""
        with self._command("M01"):
            pass
        return node

    @_decorator_insert_base_indent
    def on_m02(self, node: M02) -> M02:
        """Handle `M02` node."""
        with self._command("M02"):
            pass
        return node

    # Math

    # Math :: Operators :: Binary
    def on_add(self, node: Add) -> Add:
        """Handle `Add` node."""
        if self.explicit_parenthesis:
            self._write("(")

        node.head.visit(self)

        for operand in node.tail:
            self._write("+")
            operand.visit(self)

        if self.explicit_parenthesis:
            self._write(")")

        return node

    def on_div(self, node: Div) -> Div:
        """Handle `Div` node."""
        if self.explicit_parenthesis:
            self._write("(")

        node.head.visit(self)

        for operand in node.tail:
            self._write("/")
            operand.visit(self)

        if self.explicit_parenthesis:
            self._write(")")

        return node

    def on_mul(self, node: Mul) -> Mul:
        """Handle `Mul` node."""
        if self.explicit_parenthesis:
            self._write("(")

        node.head.visit(self)

        for operand in node.tail:
            self._write("x")
            operand.visit(self)

        if self.explicit_parenthesis:
            self._write(")")

        return node

    def on_sub(self, node: Sub) -> Sub:
        """Handle `Sub` node."""
        if self.explicit_parenthesis:
            self._write("(")

        node.head.visit(self)

        for operand in node.tail:
            self._write("-")
            operand.visit(self)

        if self.explicit_parenthesis:
            self._write(")")

        return node

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> Neg:
        """Handle `Neg` node."""
        self._write("-")
        node.operand.visit(self)
        return node

    def on_pos(self, node: Pos) -> Pos:
        """Handle `Pos` node."""
        self._write("+")
        node.operand.visit(self)
        return node

    @_decorator_insert_base_indent
    def on_assignment(self, node: Assignment) -> Assignment:
        """Handle `Assignment` node."""
        self._write(self._macro_primitive_lf)
        node.variable.visit(self)
        self._write("=")
        node.expression.visit(self)
        self._write("*")

        return node

    def on_constant(self, node: Constant) -> Constant:
        """Handle `Constant` node."""
        self._write(self._fmt_double(node.constant))
        return node

    def on_parenthesis(self, node: Parenthesis) -> Parenthesis:
        """Handle `Parenthesis` node."""
        if not self.explicit_parenthesis:
            self._write("(")

        node.inner.visit(self)

        if not self.explicit_parenthesis:
            self._write(")")

        return node

    def on_point(self, node: Point) -> Point:
        """Handle `Point` node."""
        node.x.visit(self)
        self._write(",")
        node.y.visit(self)
        return node

    def on_variable(self, node: Variable) -> Variable:
        """Handle `Variable` node."""
        self._write(node.variable)
        return node

    # Other

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:
        """Handle `Coordinate` node."""
        self._write(f"X{node.value}")
        return node

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:
        """Handle `Coordinate` node."""
        self._write(f"Y{node.value}")
        return node

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:
        """Handle `Coordinate` node."""
        self._write(f"I{node.value}")
        return node

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:
        """Handle `Coordinate` node."""
        self._write(f"J{node.value}")
        return node

    # Primitives

    @_decorator_insert_base_indent
    def on_code_0(self, node: Code0) -> Code0:
        """Handle `Code0` node."""
        self._write(f"{self._macro_primitive_lf}0{node.string}*")
        return node

    @_decorator_insert_base_indent
    def on_code_1(self, node: Code1) -> Code1:
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
        return node

    @cached_property
    def _macro_primitive_lf(self) -> str:
        if self.macro_split_mode == self.MacroSplitMode.NONE:
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
        if self.macro_split_mode in (
            self.MacroSplitMode.NONE,
            self.MacroSplitMode.PRIMITIVES,
        ):
            return ""

        if self.macro_split_mode == self.MacroSplitMode.PARAMETERS:
            return self.lf + self.macro_param_indent + self.macro_body_indent

        msg = f"Unsupported macro split mode: {self.macro_split_mode}"
        raise NotImplementedError(msg)

    @_decorator_insert_base_indent
    def on_code_2(self, node: Code2) -> Code2:
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
        return node

    @_decorator_insert_base_indent
    def on_code_4(self, node: Code4) -> Code4:
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
        return node

    @_decorator_insert_base_indent
    def on_code_5(self, node: Code5) -> Code5:
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
        return node

    @_decorator_insert_base_indent
    def on_code_6(self, node: Code6) -> Code6:
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
        return node

    @_decorator_insert_base_indent
    def on_code_7(self, node: Code7) -> Code7:
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
        return node

    @_decorator_insert_base_indent
    def on_code_20(self, node: Code20) -> Code20:
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
        return node

    @_decorator_insert_base_indent
    def on_code_21(self, node: Code21) -> Code21:
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
        return node

    @_decorator_insert_base_indent
    def on_code_22(self, node: Code22) -> Code22:
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
        return node

    # Properties

    @_decorator_insert_base_indent
    def on_as(self, node: AS) -> AS:
        """Handle `AS` node."""
        with self._extended_command("AS"):
            self._write(node.correspondence.value)
        return node

    @_decorator_insert_base_indent
    def on_fs(self, node: FS) -> FS:
        """Handle `FS` node."""
        with self._extended_command("FS"):
            self._write(node.zeros.value)
            self._write(node.coordinate_mode.value)
            self._write(f"X{node.x_integral}{node.x_decimal}")
            self._write(f"Y{node.y_integral}{node.y_decimal}")
        return node

    @_decorator_insert_base_indent
    def on_in(self, node: IN) -> IN:
        """Handle `IN` node."""
        with self._extended_command("IN"):
            self._write(node.name)
        return node

    @_decorator_insert_base_indent
    def on_ip(self, node: IP) -> IP:
        """Handle `IP` node."""
        with self._extended_command("IP"):
            self._write(node.polarity.value)
        return node

    @_decorator_insert_base_indent
    def on_ir(self, node: IR) -> IR:
        """Handle `IR` node."""
        with self._extended_command("IR"):
            self._write(self._fmt_double(node.rotation_degrees))
        return node

    @_decorator_insert_base_indent
    def on_mi(self, node: MI) -> MI:
        """Handle `MI` node."""
        with self._extended_command("MI"):
            self._write(f"A{node.a_mirroring}")
            self._write(f"B{node.b_mirroring}")
        return node

    @_decorator_insert_base_indent
    def on_mo(self, node: MO) -> MO:
        """Handle `MO` node."""
        with self._extended_command("MO"):
            self._write(node.mode.value)
        return node

    @_decorator_insert_base_indent
    def on_of(self, node: OF) -> OF:
        """Handle `OF` node."""
        with self._extended_command("OF"):
            if node.a_offset is not None:
                self._write(f"A{node.a_offset}")
            if node.b_offset is not None:
                self._write(f"B{node.b_offset}")
        return node

    @_decorator_insert_base_indent
    def on_sf(self, node: SF) -> SF:
        """Handle `SF` node."""
        with self._extended_command("SF"):
            self._write("A")
            self._write(self._fmt_double(node.a_scale))
            self._write("B")
            self._write(self._fmt_double(node.b_scale))
        return node
