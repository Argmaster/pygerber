"""`pygerber.gerberx3.visitor` contains definition of `AstVisitor` class."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygerber.gerberx3.ast.nodes import (
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
    """Interface of a node visitor.

    This class defines interface compliant with visitor pattern.
    For more information on this pattern visit:
    https://refactoring.guru/design-patterns/visitor
    """

    # Aperture

    def on_ab(self, node: AB) -> None:
        """Handle `AB` root node."""
        node.open.visit(self)
        for inner_node in node.nodes:
            inner_node.visit(self)
        node.close.visit(self)

    def on_ab_close(self, node: ABclose) -> None:
        """Handle `ABclose` node."""

    def on_ab_open(self, node: ABopen) -> None:
        """Handle `ABopen` node."""

    def on_ad(self, node: AD) -> None:
        """Handle `AD` node."""

    def on_adc(self, node: ADC) -> None:
        """Handle `AD` circle node."""
        self.on_ad(node)

    def on_adr(self, node: ADR) -> None:
        """Handle `AD` rectangle node."""
        self.on_ad(node)

    def on_ado(self, node: ADO) -> None:
        """Handle `AD` obround node."""
        self.on_ad(node)

    def on_adp(self, node: ADP) -> None:
        """Handle `AD` polygon node."""
        self.on_ad(node)

    def on_ad_macro(self, node: ADmacro) -> None:
        """Handle `AD` macro node."""
        self.on_ad(node)

    def on_am(self, node: AM) -> None:
        """Handle `AM` root node."""
        node.open.visit(self)
        for primitive in node.primitives:
            primitive.visit(self)
        node.close.visit(self)

    def on_am_close(self, node: AMclose) -> None:
        """Handle `AMclose` node."""

    def on_am_open(self, node: AMopen) -> None:
        """Handle `AMopen` node."""

    def on_sr(self, node: SR) -> None:
        """Handle `SR` root node."""
        node.open.visit(self)
        for inner_node in node.nodes:
            inner_node.visit(self)
        node.close.visit(self)

    def on_sr_close(self, node: SRclose) -> None:
        """Handle `SRclose` node."""

    def on_sr_open(self, node: SRopen) -> None:
        """Handle `SRopen` node."""

    # Attribute

    def on_ta(self, node: TA) -> None:
        """Handle `TA` node."""

    def on_ta_user_name(self, node: TA_UserName) -> None:
        """Handle `TA_UserName` node."""
        self.on_ta(node)

    def on_ta_aper_function(self, node: TA_AperFunction) -> None:
        """Handle `TA_AperFunction` node."""
        self.on_ta(node)

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> None:
        """Handle `TA_DrillTolerance` node."""
        self.on_ta(node)

    def on_ta_flash_text(self, node: TA_FlashText) -> None:
        """Handle `TA_FlashText` node."""
        self.on_ta(node)

    def on_td(self, node: TD) -> None:
        """Handle `TD` node."""

    def on_tf(self, node: TF) -> None:
        """Handle `TF` node."""

    def on_tf_user_name(self, node: TF_UserName) -> None:
        """Handle `TF_UserName` node."""
        self.on_tf(node)

    def on_tf_part(self, node: TF_Part) -> None:
        """Handle `TF_Part` node."""
        self.on_tf(node)

    def on_tf_file_function(self, node: TF_FileFunction) -> None:
        """Handle `TF_FileFunction` node."""
        self.on_tf(node)

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> None:
        """Handle `TF_FilePolarity` node."""
        self.on_tf(node)

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> None:
        """Handle `TF_SameCoordinates` node."""
        self.on_tf(node)

    def on_tf_creation_date(self, node: TF_CreationDate) -> None:
        """Handle `TF_CreationDate` node."""
        self.on_tf(node)

    def on_tf_generation_software(self, node: TF_GenerationSoftware) -> None:
        """Handle `TF_GenerationSoftware` node."""
        self.on_tf(node)

    def on_tf_project_id(self, node: TF_ProjectId) -> None:
        """Handle `TF_ProjectId` node."""
        self.on_tf(node)

    def on_tf_md5(self, node: TF_MD5) -> None:
        """Handle `TF_MD5` node."""
        self.on_tf(node)

    def on_to(self, node: TO) -> None:
        """Handle `TO` node."""

    def on_to_user_name(self, node: TO_UserName) -> None:
        """Handle `TO_UserName` node."""
        self.on_to(node)

    def on_to_n(self, node: TO_N) -> None:
        """Handle `TO_N` node."""
        self.on_to(node)

    def on_to_p(self, node: TO_P) -> None:
        """Handle `TO_P` node`."""
        self.on_to(node)

    def on_to_c(self, node: TO_C) -> None:
        """Handle `TO_C` node."""
        self.on_to(node)

    def on_to_crot(self, node: TO_CRot) -> None:
        """Handle `TO_CRot` node."""
        self.on_to(node)

    def on_to_cmfr(self, node: TO_CMfr) -> None:
        """Handle `TO_CMfr` node."""
        self.on_to(node)

    def on_to_cmnp(self, node: TO_CMNP) -> None:
        """Handle `TO_CMNP` node."""
        self.on_to(node)

    def on_to_cval(self, node: TO_CVal) -> None:
        """Handle `TO_CVal` node."""
        self.on_to(node)

    def on_to_cmnt(self, node: TO_CMnt) -> None:
        """Handle `TO_CVal` node."""
        self.on_to(node)

    def on_to_cftp(self, node: TO_CFtp) -> None:
        """Handle `TO_Cftp` node."""
        self.on_to(node)

    def on_to_cpgn(self, node: TO_CPgN) -> None:
        """Handle `TO_CPgN` node."""
        self.on_to(node)

    def on_to_cpgd(self, node: TO_CPgD) -> None:
        """Handle `TO_CPgD` node."""
        self.on_to(node)

    def on_to_chgt(self, node: TO_CHgt) -> None:
        """Handle `TO_CHgt` node."""
        self.on_to(node)

    def on_to_clbn(self, node: TO_CLbN) -> None:
        """Handle `TO_CLbN` node."""
        self.on_to(node)

    def on_to_clbd(self, node: TO_CLbD) -> None:
        """Handle `TO_CLbD` node."""
        self.on_to(node)

    def on_to_csup(self, node: TO_CSup) -> None:
        """Handle `TO_CSup` node."""
        self.on_to(node)

    # D codes

    def on_d01(self, node: D01) -> None:
        """Handle `D01` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

        if node.i is not None:
            node.i.visit(self)

        if node.j is not None:
            node.j.visit(self)

    def on_d02(self, node: D02) -> None:
        """Handle `D02` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

    def on_d03(self, node: D03) -> None:
        """Handle `D03` node."""
        if node.x is not None:
            node.x.visit(self)

        if node.y is not None:
            node.y.visit(self)

    def on_dnn(self, node: Dnn) -> None:
        """Handle `Dnn` node."""

    # G codes

    def on_g01(self, node: G01) -> None:
        """Handle `G01` node."""

    def on_g02(self, node: G02) -> None:
        """Handle `G02` node."""

    def on_g03(self, node: G03) -> None:
        """Handle `G03` node."""

    def on_g04(self, node: G04) -> None:
        """Handle `G04` node."""

    def on_g36(self, node: G36) -> None:
        """Handle `G36` node."""

    def on_g37(self, node: G37) -> None:
        """Handle `G37` node."""

    def on_g54(self, node: G54) -> None:
        """Handle `G54` node."""

    def on_g55(self, node: G55) -> None:
        """Handle `G55` node."""

    def on_g70(self, node: G70) -> None:
        """Handle `G70` node."""

    def on_g71(self, node: G71) -> None:
        """Handle `G71` node."""

    def on_g74(self, node: G74) -> None:
        """Handle `G74` node."""

    def on_g75(self, node: G75) -> None:
        """Handle `G75` node."""

    def on_g90(self, node: G90) -> None:
        """Handle `G90` node."""

    def on_g91(self, node: G91) -> None:
        """Handle `G91` node."""

    # Load

    def on_lm(self, node: LM) -> None:
        """Handle `LM` node."""

    def on_ln(self, node: LN) -> None:
        """Handle `LN` node."""

    def on_lp(self, node: LP) -> None:
        """Handle `LP` node."""

    def on_lr(self, node: LR) -> None:
        """Handle `LR` node."""

    def on_ls(self, node: LS) -> None:
        """Handle `LS` node."""

    # M Codes

    def on_m00(self, node: M00) -> None:
        """Handle `M00` node."""

    def on_m01(self, node: M01) -> None:
        """Handle `M01` node."""

    def on_m02(self, node: M02) -> None:
        """Handle `M02` node."""

    # Math

    # Math :: Operators :: Binary

    def on_add(self, node: Add) -> None:
        """Handle `Add` node."""
        self.on_expression(node)
        node.head.visit(self)
        for operand in node.tail:
            operand.visit(self)

    def on_div(self, node: Div) -> None:
        """Handle `Div` node."""
        self.on_expression(node)
        node.head.visit(self)
        for operand in node.tail:
            operand.visit(self)

    def on_mul(self, node: Mul) -> None:
        """Handle `Mul` node."""
        self.on_expression(node)
        node.head.visit(self)
        for operand in node.tail:
            operand.visit(self)

    def on_sub(self, node: Sub) -> None:
        """Handle `Sub` node."""
        self.on_expression(node)
        node.head.visit(self)
        for operand in node.tail:
            operand.visit(self)

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> None:
        """Handle `Neg` node."""
        self.on_expression(node)
        node.operand.visit(self)

    def on_pos(self, node: Pos) -> None:
        """Handle `Pos` node."""
        self.on_expression(node)
        node.operand.visit(self)

    def on_assignment(self, node: Assignment) -> None:
        """Handle `Assignment` node."""
        node.variable.visit(self)
        node.expression.visit(self)

    def on_constant(self, node: Constant) -> None:
        """Handle `Constant` node."""
        self.on_expression(node)

    def on_expression(self, node: Expression) -> None:
        """Handle `Expression` node."""

    def on_parenthesis(self, node: Parenthesis) -> None:
        """Handle `Parenthesis` node."""
        node.inner.visit(self)

    def on_point(self, node: Point) -> None:
        """Handle `Point` node."""
        node.x.visit(self)
        node.y.visit(self)

    def on_variable(self, node: Variable) -> None:
        """Handle `Variable` node."""
        self.on_expression(node)

    # Other

    def on_coordinate(self, node: Coordinate) -> None:
        """Handle `Coordinate` node."""

    def on_coordinate_x(self, node: CoordinateX) -> None:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)

    def on_coordinate_y(self, node: CoordinateY) -> None:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)

    def on_coordinate_i(self, node: CoordinateI) -> None:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)

    def on_coordinate_j(self, node: CoordinateJ) -> None:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)

    # Primitives

    def on_code_0(self, node: Code0) -> None:
        """Handle `Code0` node."""

    def on_code_1(self, node: Code1) -> None:
        """Handle `Code1` node."""
        node.exposure.visit(self)
        node.diameter.visit(self)
        node.center_x.visit(self)
        node.center_y.visit(self)
        if node.rotation is not None:
            node.rotation.visit(self)

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

    # Properties

    def on_as(self, node: AS) -> None:
        """Handle `AS` node."""

    def on_fs(self, node: FS) -> None:
        """Handle `FS` node."""

    def on_in(self, node: IN) -> None:
        """Handle `IN` node."""

    def on_ip(self, node: IP) -> None:
        """Handle `IP` node."""

    def on_ir(self, node: IR) -> None:
        """Handle `IR` node."""

    def on_mi(self, node: MI) -> None:
        """Handle `MI` node."""

    def on_mo(self, node: MO) -> None:
        """Handle `MO` node."""

    def on_of(self, node: OF) -> None:
        """Handle `OF` node."""

    def on_sf(self, node: SF) -> None:
        """Handle `SF` node."""

    # Root node

    def on_file(self, node: File) -> None:
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

    def on_end_of_file(self, node: File) -> None:
        """Handle end of file."""

    def on_exception(self, node: Node, exception: Exception) -> bool:  # noqa: ARG002
        """Handle exception.

        If return value is True, exception will be re-raised.
        """
        return True
