"""`event_ast_visitor` module contains definition of EventAstVisitor class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from pygerber.gerber.ast import AstVisitor
from pygerber.gerber.ast.nodes import Node

if TYPE_CHECKING:
    from pygerber.gerber.ast.nodes import (
        AB,
        AD,
        ADC,
        ADO,
        ADP,
        ADR,
        AM,
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
        SR,
        TA,
        TD,
        TF,
        TF_MD5,
        TO,
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
        Coordinate,
        CoordinateI,
        CoordinateJ,
        CoordinateX,
        CoordinateY,
        Div,
        Dnn,
        Expression,
        File,
        Invalid,
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


class EventAstVisitor(AstVisitor):
    """EventAstVisitor class is a specialization of AstVisitor which sends a visit event
    to every listener which subscribed to event of visiting particular node.
    """

    def __init__(self) -> None:
        super().__init__()
        self.listeners: dict[type[Node], list[Callable[[Node], None]]] = {}

    def register_listener(self, node_type: type[Node], listener: Callable) -> None:
        """Register a listener for a particular node type."""
        listeners = self.listeners.get(node_type, [])
        listeners.append(listener)
        self.listeners[node_type] = listeners

    def _trigger_listeners(self, node: Node) -> None:
        listeners = self.listeners.get(type(node), None)
        if listeners is not None:
            for listener in listeners:
                listener(node)

    def on_ab(self, node: AB) -> AB:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ab(node)

    def on_ab_close(self, node: ABclose) -> ABclose:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ab_close(node)

    def on_ab_open(self, node: ABopen) -> ABopen:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ab_open(node)

    def on_ad(self, node: AD) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ad(node)

    def on_adc(self, node: ADC) -> ADC:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_adc(node)

    def on_adr(self, node: ADR) -> ADR:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_adr(node)

    def on_ado(self, node: ADO) -> ADO:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ado(node)

    def on_adp(self, node: ADP) -> ADP:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_adp(node)

    def on_ad_macro(self, node: ADmacro) -> ADmacro:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ad_macro(node)

    def on_am(self, node: AM) -> AM:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_am(node)

    def on_am_close(self, node: AMclose) -> AMclose:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_am_close(node)

    def on_am_open(self, node: AMopen) -> AMopen:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_am_open(node)

    def on_sr(self, node: SR) -> SR:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_sr(node)

    def on_sr_close(self, node: SRclose) -> SRclose:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_sr_close(node)

    def on_sr_open(self, node: SRopen) -> SRopen:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_sr_open(node)

    def on_ta(self, node: TA) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ta(node)

    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ta_user_name(node)

    def on_ta_aper_function(  # noqa: D102
        self, node: TA_AperFunction
    ) -> TA_AperFunction:
        self._trigger_listeners(node)
        return super().on_ta_aper_function(node)

    def on_ta_drill_tolerance(  # noqa: D102
        self, node: TA_DrillTolerance
    ) -> TA_DrillTolerance:
        self._trigger_listeners(node)
        return super().on_ta_drill_tolerance(node)

    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ta_flash_text(node)

    def on_td(self, node: TD) -> TD:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_td(node)

    def on_tf(self, node: TF) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_tf(node)

    def on_tf_user_name(self, node: TF_UserName) -> TF_UserName:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_tf_user_name(node)

    def on_tf_part(self, node: TF_Part) -> TF_Part:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_tf_part(node)

    def on_tf_file_function(  # noqa: D102
        self, node: TF_FileFunction
    ) -> TF_FileFunction:
        self._trigger_listeners(node)
        return super().on_tf_file_function(node)

    def on_tf_file_polarity(  # noqa: D102
        self, node: TF_FilePolarity
    ) -> TF_FilePolarity:
        self._trigger_listeners(node)
        return super().on_tf_file_polarity(node)

    def on_tf_same_coordinates(  # noqa: D102
        self, node: TF_SameCoordinates
    ) -> TF_SameCoordinates:
        self._trigger_listeners(node)
        return super().on_tf_same_coordinates(node)

    def on_tf_creation_date(  # noqa: D102
        self, node: TF_CreationDate
    ) -> TF_CreationDate:
        self._trigger_listeners(node)
        return super().on_tf_creation_date(node)

    def on_tf_generation_software(  # noqa: D102
        self, node: TF_GenerationSoftware
    ) -> TF_GenerationSoftware:
        self._trigger_listeners(node)
        return super().on_tf_generation_software(node)

    def on_tf_project_id(self, node: TF_ProjectId) -> TF_ProjectId:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_tf_project_id(node)

    def on_tf_md5(self, node: TF_MD5) -> TF_MD5:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_tf_md5(node)

    def on_to(self, node: TO) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to(node)

    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_user_name(node)

    def on_to_n(self, node: TO_N) -> TO_N:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_n(node)

    def on_to_p(self, node: TO_P) -> TO_P:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_p(node)

    def on_to_c(self, node: TO_C) -> TO_C:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_c(node)

    def on_to_crot(self, node: TO_CRot) -> TO_CRot:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_crot(node)

    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cmfr(node)

    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cmnp(node)

    def on_to_cval(self, node: TO_CVal) -> TO_CVal:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cval(node)

    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cmnt(node)

    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cftp(node)

    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cpgn(node)

    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_cpgd(node)

    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_chgt(node)

    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_clbn(node)

    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_clbd(node)

    def on_to_csup(self, node: TO_CSup) -> TO_CSup:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_to_csup(node)

    def on_d01(self, node: D01) -> D01:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_d01(node)

    def on_d02(self, node: D02) -> D02:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_d02(node)

    def on_d03(self, node: D03) -> D03:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_d03(node)

    def on_dnn(self, node: Dnn) -> Dnn:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_dnn(node)

    def on_g01(self, node: G01) -> G01:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g01(node)

    def on_g02(self, node: G02) -> G02:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g02(node)

    def on_g03(self, node: G03) -> G03:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g03(node)

    def on_g04(self, node: G04) -> G04:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g04(node)

    def on_g36(self, node: G36) -> G36:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g36(node)

    def on_g37(self, node: G37) -> G37:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g37(node)

    def on_g54(self, node: G54) -> G54:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g54(node)

    def on_g55(self, node: G55) -> G55:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g55(node)

    def on_g70(self, node: G70) -> G70:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g70(node)

    def on_g71(self, node: G71) -> G71:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g71(node)

    def on_g74(self, node: G74) -> G74:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g74(node)

    def on_g75(self, node: G75) -> G75:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g75(node)

    def on_g90(self, node: G90) -> G90:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g90(node)

    def on_g91(self, node: G91) -> G91:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_g91(node)

    def on_lm(self, node: LM) -> LM:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_lm(node)

    def on_ln(self, node: LN) -> LN:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ln(node)

    def on_lp(self, node: LP) -> LP:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_lp(node)

    def on_lr(self, node: LR) -> LR:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_lr(node)

    def on_ls(self, node: LS) -> LS:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ls(node)

    def on_m00(self, node: M00) -> M00:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_m00(node)

    def on_m01(self, node: M01) -> M01:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_m01(node)

    def on_m02(self, node: M02) -> M02:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_m02(node)

    def on_add(self, node: Add) -> Add:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_add(node)

    def on_div(self, node: Div) -> Div:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_div(node)

    def on_mul(self, node: Mul) -> Mul:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_mul(node)

    def on_sub(self, node: Sub) -> Sub:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_sub(node)

    def on_neg(self, node: Neg) -> Neg:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_neg(node)

    def on_pos(self, node: Pos) -> Pos:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_pos(node)

    def on_assignment(self, node: Assignment) -> Assignment:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_assignment(node)

    def on_constant(self, node: Constant) -> Constant:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_constant(node)

    def on_expression(self, node: Expression) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_expression(node)

    def on_parenthesis(self, node: Parenthesis) -> Parenthesis:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_parenthesis(node)

    def on_point(self, node: Point) -> Point:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_point(node)

    def on_variable(self, node: Variable) -> Variable:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_variable(node)

    def on_coordinate(self, node: Coordinate) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_coordinate(node)

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_coordinate_x(node)

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_coordinate_y(node)

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_coordinate_i(node)

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_coordinate_j(node)

    def on_code_0(self, node: Code0) -> Code0:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_0(node)

    def on_code_1(self, node: Code1) -> Code1:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_1(node)

    def on_code_2(self, node: Code2) -> Code2:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_2(node)

    def on_code_4(self, node: Code4) -> Code4:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_4(node)

    def on_code_5(self, node: Code5) -> Code5:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_5(node)

    def on_code_6(self, node: Code6) -> Code6:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_6(node)

    def on_code_7(self, node: Code7) -> Code7:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_7(node)

    def on_code_20(self, node: Code20) -> Code20:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_20(node)

    def on_code_21(self, node: Code21) -> Code21:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_21(node)

    def on_code_22(self, node: Code22) -> Code22:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_code_22(node)

    def on_as(self, node: AS) -> AS:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_as(node)

    def on_fs(self, node: FS) -> FS:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_fs(node)

    def on_in(self, node: IN) -> IN:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_in(node)

    def on_ip(self, node: IP) -> IP:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ip(node)

    def on_ir(self, node: IR) -> IR:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_ir(node)

    def on_mi(self, node: MI) -> MI:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_mi(node)

    def on_mo(self, node: MO) -> MO:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_mo(node)

    def on_of(self, node: OF) -> OF:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_of(node)

    def on_sf(self, node: SF) -> SF:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_sf(node)

    def on_file(self, node: File) -> File:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_file(node)

    def on_end_of_file(self, node: File) -> None:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_end_of_file(node)

    def on_invalid(self, node: Invalid) -> Invalid:  # noqa: D102
        self._trigger_listeners(node)
        return super().on_invalid(node)
