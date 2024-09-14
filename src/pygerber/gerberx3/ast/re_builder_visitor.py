"""`pygerber.gerberx3.visitor` contains definition of `AstVisitor` class."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from pygerber.gerberx3.ast.ast_visitor import AstVisitor
from pygerber.gerberx3.ast.nodes import (
    AB,
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


class ReBuilderSignal(Exception):  # noqa: N818
    """ReBuilder signal base class."""


class SkipCommand(ReBuilderSignal):
    """Drop command signal."""


class ReBuilderVisitor(AstVisitor):
    """The `ReBuilderVisitor` class offers and interface for rebuilding the AST.

    Rebuilding is done by visiting each node in the AST
    Process of rebuilding can be altered to change the output AST.
    During the process of rebuilding the AST, all the source_info is lost.
    """

    def __init__(self) -> None:
        self._node_stack: list[Node] = []

    @contextmanager
    def use_parent(self, node: Node) -> Generator[None, None, None]:
        """Push parent node to the stack."""
        self._node_stack.append(node)
        try:
            yield
        finally:
            self._node_stack.pop()

    @property
    def parent(self) -> Node:
        """Get current parent node."""
        assert len(self._node_stack) > 0, "No parent node in the stack."
        return self._node_stack[-1]

    def rebuild(self, node: File) -> File:
        """Rebuild the AST."""
        return node.visit(self)

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` root node."""
        with self.use_parent(node):
            return AB(
                open=node.open.visit(self),
                nodes=[inner_node.visit(self) for inner_node in node.nodes],
                close=node.close.visit(self),
            )

    def on_ab_close(self, node: ABclose) -> ABclose:  # noqa: ARG002
        """Handle `ABclose` node."""
        return ABclose()

    def on_ab_open(self, node: ABopen) -> ABopen:
        """Handle `ABopen` node."""
        return ABopen(aperture_id=node.aperture_id)

    def on_adc(self, node: ADC) -> ADC:
        """Handle `AD` circle node."""
        self.on_ad(node)
        return ADC(
            aperture_id=node.aperture_id,
            diameter=node.diameter,
            hole_diameter=node.hole_diameter,
        )

    def on_adr(self, node: ADR) -> ADR:
        """Handle `AD` rectangle node."""
        self.on_ad(node)
        return ADR(
            aperture_id=node.aperture_id,
            width=node.width,
            height=node.height,
            hole_diameter=node.hole_diameter,
        )

    def on_ado(self, node: ADO) -> ADO:
        """Handle `AD` obround node."""
        self.on_ad(node)
        return ADO(
            aperture_id=node.aperture_id,
            width=node.width,
            height=node.height,
            hole_diameter=node.hole_diameter,
        )

    def on_adp(self, node: ADP) -> ADP:
        """Handle `AD` polygon node."""
        self.on_ad(node)
        return ADP(
            aperture_id=node.aperture_id,
            outer_diameter=node.outer_diameter,
            vertices=node.vertices,
            rotation=node.outer_diameter,
            hole_diameter=node.outer_diameter,
        )

    def on_ad_macro(self, node: ADmacro) -> ADmacro:
        """Handle `AD` macro node."""
        self.on_ad(node)
        return ADmacro(aperture_id=node.aperture_id, name=node.name, params=node.params)

    def on_am(self, node: AM) -> AM:
        """Handle `AM` root node."""
        with self.use_parent(node):
            return AM(
                open=node.open.visit(self),
                primitives=[p.visit(self) for p in node.primitives],
                close=node.close.visit(self),
            )

    def on_am_close(self, node: AMclose) -> AMclose:  # noqa: ARG002
        """Handle `AMclose` node."""
        return AMclose()

    def on_am_open(self, node: AMopen) -> AMopen:
        """Handle `AMopen` node."""
        return AMopen(name=node.name)

    def on_sr(self, node: SR) -> SR:
        """Handle `SR` root node."""
        with self.use_parent(node):
            return SR(
                open=node.open.visit(self),
                nodes=[inner_node.visit(self) for inner_node in node.nodes],
                close=node.close.visit(self),
            )

    def on_sr_close(self, node: SRclose) -> SRclose:  # noqa: ARG002
        """Handle `SRclose` node."""
        return SRclose()

    def on_sr_open(self, node: SRopen) -> SRopen:
        """Handle `SRopen` node."""
        return SRopen(x=node.x, y=node.y, i=node.i, j=node.j)

    # Attribute

    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:
        """Handle `TA_UserName` node."""
        self.on_ta(node)
        return TA_UserName(user_name=node.user_name, fields=node.fields.copy())

    def on_ta_aper_function(self, node: TA_AperFunction) -> TA_AperFunction:
        """Handle `TA_AperFunction` node."""
        self.on_ta(node)
        return TA_AperFunction(function=node.function, fields=node.fields.copy())

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> TA_DrillTolerance:
        """Handle `TA_DrillTolerance` node."""
        self.on_ta(node)
        return TA_DrillTolerance(
            plus_tolerance=node.plus_tolerance, minus_tolerance=node.minus_tolerance
        )

    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:
        """Handle `TA_FlashText` node."""
        self.on_ta(node)
        return TA_FlashText(
            string=node.string,
            mode=node.mode,
            mirroring=node.mirroring,
            font=node.font,
            size=node.size,
            comments=node.comments,
        )

    def on_td(self, node: TD) -> TD:
        """Handle `TD` node."""
        return TD(name=node.name)

    def on_tf_user_name(self, node: TF_UserName) -> TF_UserName:
        """Handle `TF_UserName` node."""
        self.on_tf(node)
        return TF_UserName(user_name=node.user_name, fields=node.fields.copy())

    def on_tf_part(self, node: TF_Part) -> TF_Part:
        """Handle `TF_Part` node."""
        self.on_tf(node)
        return TF_Part(part=node.part, fields=node.fields.copy())

    def on_tf_file_function(self, node: TF_FileFunction) -> TF_FileFunction:
        """Handle `TF_FileFunction` node."""
        self.on_tf(node)
        return TF_FileFunction(
            file_function=node.file_function, fields=node.fields.copy()
        )

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> TF_FilePolarity:
        """Handle `TF_FilePolarity` node."""
        self.on_tf(node)
        return TF_FilePolarity(polarity=node.polarity)

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> TF_SameCoordinates:
        """Handle `TF_SameCoordinates` node."""
        self.on_tf(node)
        return TF_SameCoordinates(identifier=node.identifier)

    def on_tf_creation_date(self, node: TF_CreationDate) -> TF_CreationDate:
        """Handle `TF_CreationDate` node."""
        self.on_tf(node)
        return TF_CreationDate(creation_date=node.creation_date)

    def on_tf_generation_software(
        self, node: TF_GenerationSoftware
    ) -> TF_GenerationSoftware:
        """Handle `TF_GenerationSoftware` node."""
        self.on_tf(node)
        return TF_GenerationSoftware(
            vendor=node.vendor, application=node.application, version=node.version
        )

    def on_tf_project_id(self, node: TF_ProjectId) -> TF_ProjectId:
        """Handle `TF_ProjectId` node."""
        self.on_tf(node)
        return TF_ProjectId(name=node.name, guid=node.guid, revision=node.revision)

    def on_tf_md5(self, node: TF_MD5) -> TF_MD5:
        """Handle `TF_MD5` node."""
        self.on_tf(node)
        return TF_MD5(md5=node.md5)

    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:
        """Handle `TO_UserName` node."""
        self.on_to(node)
        return TO_UserName(user_name=node.user_name, fields=node.fields.copy())

    def on_to_n(self, node: TO_N) -> TO_N:
        """Handle `TO_N` node."""
        self.on_to(node)
        return TO_N(net_names=node.net_names.copy())

    def on_to_p(self, node: TO_P) -> TO_P:
        """Handle `TO_P` node`."""
        self.on_to(node)
        return TO_P(function=node.function, number=node.number, refdes=node.refdes)

    def on_to_c(self, node: TO_C) -> TO_C:
        """Handle `TO_C` node."""
        self.on_to(node)
        return TO_C(refdes=node.refdes)

    def on_to_crot(self, node: TO_CRot) -> TO_CRot:
        """Handle `TO_CRot` node."""
        self.on_to(node)
        return TO_CRot(angle=node.angle)

    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:
        """Handle `TO_CMfr` node."""
        self.on_to(node)
        return TO_CMfr(manufacturer=node.manufacturer)

    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:
        """Handle `TO_CMNP` node."""
        self.on_to(node)
        return TO_CMNP(part_number=node.part_number)

    def on_to_cval(self, node: TO_CVal) -> TO_CVal:
        """Handle `TO_CVal` node."""
        self.on_to(node)
        return TO_CVal(value=node.value)

    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:
        """Handle `TO_CVal` node."""
        self.on_to(node)
        return TO_CMnt(mount=node.mount)

    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:
        """Handle `TO_Cftp` node."""
        self.on_to(node)
        return TO_CFtp(footprint=node.footprint)

    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:
        """Handle `TO_CPgN` node."""
        self.on_to(node)
        return TO_CPgN(name=node.name)

    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:
        """Handle `TO_CPgD` node."""
        self.on_to(node)
        return TO_CPgD(description=node.description)

    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:
        """Handle `TO_CHgt` node."""
        self.on_to(node)
        return TO_CHgt(height=node.height)

    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:
        """Handle `TO_CLbN` node."""
        self.on_to(node)
        return TO_CLbN(name=node.name)

    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:
        """Handle `TO_CLbD` node."""
        self.on_to(node)
        return TO_CLbD(description=node.description)

    def on_to_csup(self, node: TO_CSup) -> TO_CSup:
        """Handle `TO_CSup` node."""
        self.on_to(node)
        return TO_CSup(
            supplier=node.supplier,
            supplier_part=node.supplier_part,
            other_suppliers=node.other_suppliers.copy(),
        )

    # D codes

    def on_d01(self, node: D01) -> D01:
        """Handle `D01` node."""
        with self.use_parent(node):
            return D01(
                x=node.x.visit(self) if node.x is not None else None,
                y=node.y.visit(self) if node.y is not None else None,
                i=node.i.visit(self) if node.i is not None else None,
                j=node.j.visit(self) if node.j is not None else None,
            )

    def on_d02(self, node: D02) -> D02:
        """Handle `D02` node."""
        with self.use_parent(node):
            return D02(
                x=node.x.visit(self) if node.x is not None else None,
                y=node.y.visit(self) if node.y is not None else None,
            )

    def on_d03(self, node: D03) -> D03:
        """Handle `D03` node."""
        with self.use_parent(node):
            return D03(
                x=node.x.visit(self) if node.x is not None else None,
                y=node.y.visit(self) if node.y is not None else None,
            )

    def on_dnn(self, node: Dnn) -> Dnn:
        """Handle `Dnn` node."""
        return Dnn(aperture_id=node.aperture_id, is_standalone=node.is_standalone)

    # G codes

    def on_g01(self, node: G01) -> G01:  # noqa: ARG002
        """Handle `G01` node."""
        return G01()

    def on_g02(self, node: G02) -> G02:  # noqa: ARG002
        """Handle `G02` node."""
        return G02()

    def on_g03(self, node: G03) -> G03:  # noqa: ARG002
        """Handle `G03` node."""
        return G03()

    def on_g04(self, node: G04) -> G04:  # noqa: ARG002
        """Handle `G04` node."""
        return G04()

    def on_g36(self, node: G36) -> G36:  # noqa: ARG002
        """Handle `G36` node."""
        return G36()

    def on_g37(self, node: G37) -> G37:  # noqa: ARG002
        """Handle `G37` node."""
        return G37()

    def on_g54(self, node: G54) -> G54:  # noqa: ARG002
        """Handle `G54` node."""
        return G54()

    def on_g55(self, node: G55) -> G55:  # noqa: ARG002
        """Handle `G55` node."""
        return G55()

    def on_g70(self, node: G70) -> G70:  # noqa: ARG002
        """Handle `G70` node."""
        return G70()

    def on_g71(self, node: G71) -> G71:  # noqa: ARG002
        """Handle `G71` node."""
        return G71()

    def on_g74(self, node: G74) -> G74:  # noqa: ARG002
        """Handle `G74` node."""
        return G74()

    def on_g75(self, node: G75) -> G75:  # noqa: ARG002
        """Handle `G75` node."""
        return G75()

    def on_g90(self, node: G90) -> G90:  # noqa: ARG002
        """Handle `G90` node."""
        return G90()

    def on_g91(self, node: G91) -> G91:  # noqa: ARG002
        """Handle `G91` node."""
        return G91()

    # Load

    def on_lm(self, node: LM) -> LM:
        """Handle `LM` node."""
        return LM(mirroring=node.mirroring)

    def on_ln(self, node: LN) -> LN:
        """Handle `LN` node."""
        return LN(name=node.name)

    def on_lp(self, node: LP) -> LP:
        """Handle `LP` node."""
        return LP(polarity=node.polarity)

    def on_lr(self, node: LR) -> LR:
        """Handle `LR` node."""
        return LR(rotation=node.rotation)

    def on_ls(self, node: LS) -> LS:
        """Handle `LS` node."""
        return LS(scale=node.scale)

    # M Codes

    def on_m00(self, node: M00) -> M00:  # noqa: ARG002
        """Handle `M00` node."""
        return M00()

    def on_m01(self, node: M01) -> M01:  # noqa: ARG002
        """Handle `M01` node."""
        return M01()

    def on_m02(self, node: M02) -> M02:  # noqa: ARG002
        """Handle `M02` node."""
        return M02()

    # Math

    # Math :: Operators :: Binary

    def on_add(self, node: Add) -> Add:
        """Handle `Add` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Add(
                head=node.head.visit(self),
                tail=[operand.visit(self) for operand in node.tail],
            )

    def on_div(self, node: Div) -> Div:
        """Handle `Div` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Div(
                head=node.head.visit(self),
                tail=[operand.visit(self) for operand in node.tail],
            )

    def on_mul(self, node: Mul) -> Mul:
        """Handle `Mul` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Mul(
                head=node.head.visit(self),
                tail=[operand.visit(self) for operand in node.tail],
            )

    def on_sub(self, node: Sub) -> Sub:
        """Handle `Sub` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Sub(
                head=node.head.visit(self),
                tail=[operand.visit(self) for operand in node.tail],
            )

    # Math :: Operators :: Unary

    def on_neg(self, node: Neg) -> Neg:
        """Handle `Neg` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Neg(operand=node.operand.visit(self))

    def on_pos(self, node: Pos) -> Pos:
        """Handle `Pos` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Pos(operand=node.operand.visit(self))

    def on_assignment(self, node: Assignment) -> Assignment:
        """Handle `Assignment` node."""
        with self.use_parent(node):
            return Assignment(
                variable=node.variable.visit(self),
                expression=node.expression.visit(self),
            )

    def on_constant(self, node: Constant) -> Constant:
        """Handle `Constant` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Constant(constant=node.constant)

    def on_parenthesis(self, node: Parenthesis) -> Parenthesis:
        """Handle `Parenthesis` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Parenthesis(inner=node.inner.visit(self))

    def on_point(self, node: Point) -> Point:
        """Handle `Point` node."""
        with self.use_parent(node):
            return Point(x=node.x, y=node.y)

    def on_variable(self, node: Variable) -> Variable:
        """Handle `Variable` node."""
        self.on_expression(node)
        with self.use_parent(node):
            return Variable(variable=node.variable)

    # Other

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return CoordinateX(value=node.value)

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:
        """Handle `Coordinate` node."""
        self.on_coordinate(node)
        return CoordinateY(value=node.value)

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:
        """Handle `Coordinate` node."""
        return CoordinateI(value=node.value)

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:
        """Handle `Coordinate` node."""
        return CoordinateJ(value=node.value)

    # Primitives

    def on_code_0(self, node: Code0) -> Code0:
        """Handle `Code0` node."""
        with self.use_parent(node):
            return Code0(string=node.string)

    def on_code_1(self, node: Code1) -> Code1:
        """Handle `Code1` node."""
        with self.use_parent(node):
            return Code1(
                exposure=node.exposure.visit(self),
                diameter=node.diameter.visit(self),
                center_x=node.center_x.visit(self),
                center_y=node.center_y.visit(self),
                rotation=(
                    node.rotation.visit(self) if node.rotation is not None else None
                ),
            )

    def on_code_2(self, node: Code2) -> Code2:
        """Handle `Code2` node."""
        with self.use_parent(node):
            return Code2(
                exposure=node.exposure.visit(self),
                width=node.width.visit(self),
                start_x=node.start_x.visit(self),
                start_y=node.start_y.visit(self),
                end_x=node.end_x.visit(self),
                end_y=node.end_y.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_4(self, node: Code4) -> Code4:
        """Handle `Code4` node."""
        with self.use_parent(node):
            return Code4(
                exposure=node.exposure.visit(self),
                number_of_points=node.number_of_points.visit(self),
                start_x=node.start_x.visit(self),
                start_y=node.start_y.visit(self),
                points=[point.visit(self) for point in node.points],
                rotation=node.rotation.visit(self),
            )

    def on_code_5(self, node: Code5) -> Code5:
        """Handle `Code5` node."""
        with self.use_parent(node):
            return Code5(
                exposure=node.exposure.visit(self),
                number_of_vertices=node.number_of_vertices.visit(self),
                center_x=node.center_x.visit(self),
                center_y=node.center_y.visit(self),
                diameter=node.diameter.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_6(self, node: Code6) -> Code6:
        """Handle `Code6` node."""
        with self.use_parent(node):
            return Code6(
                center_x=node.center_x.visit(self),
                center_y=node.center_y.visit(self),
                outer_diameter=node.outer_diameter.visit(self),
                ring_thickness=node.ring_thickness.visit(self),
                gap_between_rings=node.gap_between_rings.visit(self),
                max_ring_count=node.max_ring_count.visit(self),
                crosshair_thickness=node.crosshair_thickness.visit(self),
                crosshair_length=node.crosshair_length.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_7(self, node: Code7) -> Code7:
        """Handle `Code7` node."""
        with self.use_parent(node):
            return Code7(
                center_x=node.center_x.visit(self),
                center_y=node.center_y.visit(self),
                outer_diameter=node.outer_diameter.visit(self),
                inner_diameter=node.inner_diameter.visit(self),
                gap_thickness=node.gap_thickness.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_20(self, node: Code20) -> Code20:
        """Handle `Code20` node."""
        with self.use_parent(node):
            return Code20(
                exposure=node.exposure.visit(self),
                width=node.width.visit(self),
                start_x=node.start_x.visit(self),
                start_y=node.start_y.visit(self),
                end_x=node.end_x.visit(self),
                end_y=node.end_y.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_21(self, node: Code21) -> Code21:
        """Handle `Code21` node."""
        with self.use_parent(node):
            return Code21(
                exposure=node.exposure.visit(self),
                width=node.width.visit(self),
                height=node.height.visit(self),
                center_x=node.center_x.visit(self),
                center_y=node.center_y.visit(self),
                rotation=node.rotation.visit(self),
            )

    def on_code_22(self, node: Code22) -> Code22:
        """Handle `Code22` node."""
        with self.use_parent(node):
            return Code22(
                exposure=node.exposure.visit(self),
                width=node.width.visit(self),
                height=node.height.visit(self),
                x_lower_left=node.x_lower_left.visit(self),
                y_lower_left=node.y_lower_left.visit(self),
                rotation=node.rotation.visit(self),
            )

    # Properties

    def on_as(self, node: AS) -> AS:
        """Handle `AS` node."""
        return AS(correspondence=node.correspondence)

    def on_fs(self, node: FS) -> FS:
        """Handle `FS` node."""
        return FS(
            zeros=node.zeros,
            coordinate_mode=node.coordinate_mode,
            x_integral=node.x_integral,
            x_decimal=node.x_decimal,
            y_integral=node.y_integral,
            y_decimal=node.y_decimal,
        )

    def on_in(self, node: IN) -> IN:
        """Handle `IN` node."""
        return IN(name=node.name)

    def on_ip(self, node: IP) -> IP:
        """Handle `IP` node."""
        return IP(polarity=node.polarity)

    def on_ir(self, node: IR) -> IR:
        """Handle `IR` node."""
        return IR(rotation_degrees=node.rotation_degrees)

    def on_mi(self, node: MI) -> MI:
        """Handle `MI` node."""
        return MI(a_mirroring=node.a_mirroring, b_mirroring=node.b_mirroring)

    def on_mo(self, node: MO) -> MO:
        """Handle `MO` node."""
        return MO(mode=node.mode)

    def on_of(self, node: OF) -> OF:
        """Handle `OF` node."""
        return OF(a_offset=node.a_offset, b_offset=node.b_offset)

    def on_sf(self, node: SF) -> SF:
        """Handle `SF` node."""
        return SF(a_scale=node.a_scale, b_scale=node.b_scale)

    # Root node

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        assert len(self._node_stack) <= 0, "File node cannot have a parent."

        with self.use_parent(node):
            self.commands = []
            try:
                for command in node.nodes:
                    try:
                        self.commands.append(command.visit(self))
                    except SkipCommand:  # noqa: PERF203
                        pass

                    except Exception as e:
                        if self.on_exception(command, e):
                            raise
            finally:
                self.on_end_of_file(node)

            return File(nodes=self.commands)
