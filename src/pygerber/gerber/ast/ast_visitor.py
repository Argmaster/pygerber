"""The `ast_visitor` module contains `AstVisitor` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pygerber.gerber.ast.nodes.invalid import Invalid

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


class AstVisitor:
    """The `AstVisitor` class is a class that acts as a visitor for `Node` instances
    according to the visitor design pattern.

    For more information on this pattern visit:
    https://refactoring.guru/design-patterns/visitor

    Logic of walking the AST is implemented within the visitor callbacks, hence be
    careful when overriding methods of this class, as not calling `super().method()` may
    result in subnodes of a node not being visited at all. This applies to nodes
    like `AB`, `AM` etc. Whenever you override a method, look up the implementation from
    AstVisitor to make sure you will be getting the behavior you intend to get.
    """

    # Aperture

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` root node."""
        node.open.visit(self)
        for inner_node in node.nodes:
            inner_node.visit(self)
        node.close.visit(self)

        return node

    def on_ab_close(self, node: ABclose) -> ABclose:
        """Handle `ABclose` node."""
        return node

    def on_ab_open(self, node: ABopen) -> ABopen:
        """Handle `ABopen` node."""
        return node

    def on_ad(self, node: AD) -> None:
        """Handle `AD` node."""

    def on_adc(self, node: ADC) -> ADC:
        """Handle `AD` circle node."""
        self.on_ad(node)
        return node

    def on_adr(self, node: ADR) -> ADR:
        """Handle `AD` rectangle node."""
        self.on_ad(node)
        return node

    def on_ado(self, node: ADO) -> ADO:
        """Handle `AD` obround node."""
        self.on_ad(node)
        return node

    def on_adp(self, node: ADP) -> ADP:
        """Handle `AD` polygon node."""
        self.on_ad(node)
        return node

    def on_ad_macro(self, node: ADmacro) -> ADmacro:
        """Handle `AD` macro node."""
        self.on_ad(node)
        return node

    def on_am(self, node: AM) -> AM:
        """Handle `AM` root node."""
        node.open.visit(self)
        for primitive in node.primitives:
            primitive.visit(self)
        node.close.visit(self)
        return node

    def on_am_close(self, node: AMclose) -> AMclose:
        """Handle `AMclose` node."""
        return node

    def on_am_open(self, node: AMopen) -> AMopen:
        """Handle `AMopen` node."""
        return node

    def on_sr(self, node: SR) -> SR:
        """Handle `SR` root node."""
        node.open.visit(self)
        for inner_node in node.nodes:
            inner_node.visit(self)
        node.close.visit(self)
        return node

    def on_sr_close(self, node: SRclose) -> SRclose:
        """Handle `SRclose` node."""
        return node

    def on_sr_open(self, node: SRopen) -> SRopen:
        """Handle `SRopen` node."""
        return node

    # Attribute

    def on_ta(self, node: TA) -> None:
        """Handle `TA` node."""

    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:
        """Handle `TA_UserName` node."""
        self.on_ta(node)
        return node

    def on_ta_aper_function(self, node: TA_AperFunction) -> TA_AperFunction:
        """Handle `TA_AperFunction` node."""
        self.on_ta(node)
        return node

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> TA_DrillTolerance:
        """Handle `TA_DrillTolerance` node."""
        self.on_ta(node)
        return node

    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:
        """Handle `TA_FlashText` node."""
        self.on_ta(node)
        return node

    def on_td(self, node: TD) -> TD:
        """Handle `TD` node."""
        return node

    def on_tf(self, node: TF) -> None:
        """Handle `TF` node."""

    def on_tf_user_name(self, node: TF_UserName) -> TF_UserName:
        """Handle `TF_UserName` node."""
        self.on_tf(node)
        return node

    def on_tf_part(self, node: TF_Part) -> TF_Part:
        """Handle `TF_Part` node."""
        self.on_tf(node)
        return node

    def on_tf_file_function(self, node: TF_FileFunction) -> TF_FileFunction:
        """Handle `TF_FileFunction` node."""
        self.on_tf(node)
        return node

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> TF_FilePolarity:
        """Handle `TF_FilePolarity` node."""
        self.on_tf(node)
        return node

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> TF_SameCoordinates:
        """Handle `TF_SameCoordinates` node."""
        self.on_tf(node)
        return node

    def on_tf_creation_date(self, node: TF_CreationDate) -> TF_CreationDate:
        """Handle `TF_CreationDate` node."""
        self.on_tf(node)
        return node

    def on_tf_generation_software(
        self, node: TF_GenerationSoftware
    ) -> TF_GenerationSoftware:
        """Handle `TF_GenerationSoftware` node."""
        self.on_tf(node)
        return node

    def on_tf_project_id(self, node: TF_ProjectId) -> TF_ProjectId:
        """Handle `TF_ProjectId` node."""
        self.on_tf(node)
        return node

    def on_tf_md5(self, node: TF_MD5) -> TF_MD5:
        """Handle `TF_MD5` node."""
        self.on_tf(node)
        return node

    def on_to(self, node: TO) -> None:
        """Handle `TO` node."""

    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:
        """Handle `TO_UserName` node."""
        self.on_to(node)
        return node

    def on_to_n(self, node: TO_N) -> TO_N:
        """Handle `TO_N` node."""
        self.on_to(node)
        return node

    def on_to_p(self, node: TO_P) -> TO_P:
        """Handle `TO_P` node`."""
        self.on_to(node)
        return node

    def on_to_c(self, node: TO_C) -> TO_C:
        """Handle `TO_C` node."""
        self.on_to(node)
        return node

    def on_to_crot(self, node: TO_CRot) -> TO_CRot:
        """Handle `TO_CRot` node."""
        self.on_to(node)
        return node

    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:
        """Handle `TO_CMfr` node."""
        self.on_to(node)
        return node

    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:
        """Handle `TO_CMNP` node."""
        self.on_to(node)
        return node

    def on_to_cval(self, node: TO_CVal) -> TO_CVal:
        """Handle `TO_CVal` node."""
        self.on_to(node)
        return node

    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:
        """Handle `TO_CVal` node."""
        self.on_to(node)
        return node

    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:
        """Handle `TO_Cftp` node."""
        self.on_to(node)
        return node

    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:
        """Handle `TO_CPgN` node."""
        self.on_to(node)
        return node

    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:
        """Handle `TO_CPgD` node."""
        self.on_to(node)
        return node

    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:
        """Handle `TO_CHgt` node."""
        self.on_to(node)
        return node

    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:
        """Handle `TO_CLbN` node."""
        self.on_to(node)
        return node

    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:
        """Handle `TO_CLbD` node."""
        self.on_to(node)
        return node

    def on_to_csup(self, node: TO_CSup) -> TO_CSup:
        """Handle `TO_CSup` node."""
        self.on_to(node)
        return node

    # D codes

    def on_d01(self, node: D01) -> D01:
        """Handle `D01` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

        if node.i is not None:
            node.i.visit(self)

        if node.j is not None:
            node.j.visit(self)

        return node

    def on_d02(self, node: D02) -> D02:
        """Handle `D02` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

        return node

    def on_d03(self, node: D03) -> D03:
        """Handle `D03` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

        return node

    def on_dnn(self, node: Dnn) -> Dnn:
        """Handle `Dnn` node."""
        return node

    # G codes

    def on_g01(self, node: G01) -> G01:
        """Handle `G01` node."""
        return node

    def on_g02(self, node: G02) -> G02:
        """Handle `G02` node."""
        return node

    def on_g03(self, node: G03) -> G03:
        """Handle `G03` node."""
        return node

    def on_g04(self, node: G04) -> G04:
        """Handle `G04` node."""
        return node

    def on_g36(self, node: G36) -> G36:
        """Handle `G36` node."""
        return node

    def on_g37(self, node: G37) -> G37:
        """Handle `G37` node."""
        return node

    def on_g54(self, node: G54) -> G54:
        """Handle `G54` node."""
        return node

    def on_g55(self, node: G55) -> G55:
        """Handle `G55` node."""
        return node

    def on_g70(self, node: G70) -> G70:
        """Handle `G70` node."""
        return node

    def on_g71(self, node: G71) -> G71:
        """Handle `G71` node."""
        return node

    def on_g74(self, node: G74) -> G74:
        """Handle `G74` node."""
        return node

    def on_g75(self, node: G75) -> G75:
        """Handle `G75` node."""
        return node

    def on_g90(self, node: G90) -> G90:
        """Handle `G90` node."""
        return node

    def on_g91(self, node: G91) -> G91:
        """Handle `G91` node."""
        return node

    # Load

    def on_lm(self, node: LM) -> LM:
        """Handle `LM` node."""
        return node

    def on_ln(self, node: LN) -> LN:
        """Handle `LN` node."""
        return node

    def on_lp(self, node: LP) -> LP:
        """Handle `LP` node."""
        return node

    def on_lr(self, node: LR) -> LR:
        """Handle `LR` node."""
        return node

    def on_ls(self, node: LS) -> LS:
        """Handle `LS` node."""
        return node

    # M Codes

    def on_m00(self, node: M00) -> M00:
        """Handle `M00` node."""
        return node

    def on_m01(self, node: M01) -> M01:
        """Handle `M01` node."""
        return node

    def on_m02(self, node: M02) -> M02:
        """Handle `M02` node."""
        return node

    # Math

    # Math :: Operators :: Binary

    def on_add(self, node: Add) -> Add:
        """Handle `Add` node."""
        self.on_expression(node)
        node.head.visit(self)

        for operand in node.tail:
            operand.visit(self)

        return node

    def on_div(self, node: Div) -> Div:
        """Handle `Div` node."""
        self.on_expression(node)
        node.head.visit(self)

        for operand in node.tail:
            operand.visit(self)

        return node

    def on_mul(self, node: Mul) -> Mul:
        """Handle `Mul` node."""
        self.on_expression(node)
        node.head.visit(self)

        for operand in node.tail:
            operand.visit(self)

        return node

    def on_sub(self, node: Sub) -> Sub:
        """Handle `Sub` node."""
        self.on_expression(node)
        node.head.visit(self)

        for operand in node.tail:
            operand.visit(self)

        return node

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> Neg:
        """Handle `Neg` node."""
        self.on_expression(node)
        node.operand.visit(self)
        return node

    def on_pos(self, node: Pos) -> Pos:
        """Handle `Pos` node."""
        self.on_expression(node)
        node.operand.visit(self)
        return node

    def on_assignment(self, node: Assignment) -> Assignment:
        """Handle `Assignment` node."""
        node.variable.visit(self)
        node.expression.visit(self)
        return node

    def on_constant(self, node: Constant) -> Constant:
        """Handle `Constant` node."""
        self.on_expression(node)
        return node

    def on_expression(self, node: Expression) -> None:
        """Handle `Expression` node."""

    def on_parenthesis(self, node: Parenthesis) -> Parenthesis:
        """Handle `Parenthesis` node."""
        self.on_expression(node)
        node.inner.visit(self)
        return node

    def on_point(self, node: Point) -> Point:
        """Handle `Point` node."""
        node.x.visit(self)
        node.y.visit(self)
        return node

    def on_variable(self, node: Variable) -> Variable:
        """Handle `Variable` node."""
        self.on_expression(node)
        return node

    # Other

    def on_coordinate(self, node: Coordinate) -> None:
        """Handle `Coordinate` node."""

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return node

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return node

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return node

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return node

    # Primitives

    def on_code_0(self, node: Code0) -> Code0:
        """Handle `Code0` node."""
        return node

    def on_code_1(self, node: Code1) -> Code1:
        """Handle `Code1` node."""
        node.exposure.visit(self)
        node.diameter.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        if node.rotation is not None:
            node.rotation.visit(self)
        return node

    def on_code_2(self, node: Code2) -> Code2:
        """Handle `Code2` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        node.end_x.visit(self)
        node.end_y.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_4(self, node: Code4) -> Code4:
        """Handle `Code4` node."""
        node.exposure.visit(self)
        node.number_of_points.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        for point in node.points:
            point.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_5(self, node: Code5) -> Code5:
        """Handle `Code5` node."""
        node.exposure.visit(self)
        node.number_of_vertices.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.diameter.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_6(self, node: Code6) -> Code6:
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
        return node

    def on_code_7(self, node: Code7) -> Code7:
        """Handle `Code7` node."""
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.outer_diameter.visit(self)
        node.inner_diameter.visit(self)
        node.gap_thickness.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_20(self, node: Code20) -> Code20:
        """Handle `Code20` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.start_x.visit(self)
        node.start_y.visit(self)
        node.end_x.visit(self)
        node.end_y.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_21(self, node: Code21) -> Code21:
        """Handle `Code21` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.height.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        node.rotation.visit(self)
        return node

    def on_code_22(self, node: Code22) -> Code22:
        """Handle `Code22` node."""
        node.exposure.visit(self)
        node.width.visit(self)
        node.height.visit(self)
        node.x_lower_left.visit(self)
        node.y_lower_left.visit(self)
        node.rotation.visit(self)
        return node

    # Properties

    def on_as(self, node: AS) -> AS:
        """Handle `AS` node."""
        return node

    def on_fs(self, node: FS) -> FS:
        """Handle `FS` node."""
        return node

    def on_in(self, node: IN) -> IN:
        """Handle `IN` node."""
        return node

    def on_ip(self, node: IP) -> IP:
        """Handle `IP` node."""
        return node

    def on_ir(self, node: IR) -> IR:
        """Handle `IR` node."""
        return node

    def on_mi(self, node: MI) -> MI:
        """Handle `MI` node."""
        return node

    def on_mo(self, node: MO) -> MO:
        """Handle `MO` node."""
        return node

    def on_of(self, node: OF) -> OF:
        """Handle `OF` node."""
        return node

    def on_sf(self, node: SF) -> SF:
        """Handle `SF` node."""
        return node

    # Root node

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        try:
            for command in node.nodes:
                try:
                    command.visit(self)
                except Exception as e:  # noqa: PERF203
                    if self.on_exception(command, e):
                        raise
        finally:
            self.on_end_of_file(node)
        return node

    def on_end_of_file(self, node: File) -> None:
        """Handle end of file."""

    def on_exception(self, node: Node, exception: Exception) -> bool:  # noqa: ARG002
        """Handle exception.

        If return value is True, exception will be re-raised.
        """
        return True

    def on_invalid(self, node: Invalid) -> Invalid:
        """Handle invalid node."""
        return node
