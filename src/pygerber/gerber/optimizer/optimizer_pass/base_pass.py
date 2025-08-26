"""The `base_pass` module contains the `BasePass` class."""

from __future__ import annotations

from contextlib import suppress
from typing import Optional

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes import (
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
    Invalid,
    Mul,
    Neg,
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
from pygerber.gerber.optimizer.optimizer_pass.signals import (
    DeepDiscardNode,
    ShallowDiscardNode,
)


class BasePass(AstVisitor):
    """Base class for AST optimization passes."""

    def __init__(self) -> None:
        """Initialize base pass."""
        self._original: Optional[File] = None

    @property
    def original(self) -> File:
        """Get original AST."""
        assert self._original is not None
        return self._original

    def on_ab(self, node: AB) -> AB:
        """Handle `AB` root node."""
        open_ = node.open.visit(self)
        nodes = []
        for inner_node in node.nodes:
            with suppress(ShallowDiscardNode):
                nodes.append(inner_node.visit(self))

        close = node.close.visit(self)

        return AB.model_construct(open=open_, nodes=nodes, close=close)

    def on_ab_close(self, node: ABclose) -> ABclose:  # noqa: ARG002
        """Handle `ABclose` node."""
        return ABclose()

    def on_ab_open(self, node: ABopen) -> ABopen:
        """Handle `ABopen` node."""
        return ABopen.model_construct(aperture_id=node.aperture_id)

    def on_adc(self, node: ADC) -> ADC:
        """Handle `ADC` node."""
        return ADC.model_construct(
            aperture_id=node.aperture_id,
            diameter=node.diameter,
            hole_diameter=node.hole_diameter,
        )

    def on_adr(self, node: ADR) -> ADR:
        """Handle `ADR` node."""
        return ADR.model_construct(
            aperture_id=node.aperture_id,
            width=node.width,
            height=node.height,
            hole_diameter=node.hole_diameter,
        )

    def on_ado(self, node: ADO) -> ADO:
        """Handle `ADO` node."""
        return ADO.model_construct(
            aperture_id=node.aperture_id,
            width=node.width,
            height=node.height,
            hole_diameter=node.hole_diameter,
        )

    def on_adp(self, node: ADP) -> ADP:
        """Handle `ADP` node."""
        return ADP.model_construct(
            aperture_id=node.aperture_id,
            outer_diameter=node.outer_diameter,
            vertices=node.vertices,
            rotation=node.rotation,
            hole_diameter=node.hole_diameter,
        )

    def on_ad_macro(self, node: ADmacro) -> ADmacro:
        """Handle `AD` macro node."""
        return ADmacro.model_construct(
            name=node.name,
            params=node.params,
        )

    def on_am(self, node: AM) -> AM:
        """Handle `AM` node."""
        open_ = node.open.visit(self)

        primitives = []
        for primitive in node.primitives:
            with suppress(ShallowDiscardNode):
                primitives.append(primitive.visit(self))

        close = node.close.visit(self)

        return AM.model_construct(open=open_, primitives=primitives, close=close)

    def on_am_close(self, node: AMclose) -> AMclose:  # noqa: ARG002
        """Handle `AMclose` node."""
        return AMclose()

    def on_am_open(self, node: AMopen) -> AMopen:
        """Handle `AMopen` node."""
        return AMopen.model_construct(name=node.name)

    def on_sr(self, node: SR) -> SR:
        """Handle `SR` node."""
        open_ = node.open.visit(self)

        nodes = []
        for inner_node in node.nodes:
            with suppress(ShallowDiscardNode):
                nodes.append(inner_node.visit(self))

        close = node.close.visit(self)

        return SR.model_construct(open=open_, nodes=nodes, close=close)

    def on_sr_close(self, node: SRclose) -> SRclose:  # noqa: ARG002
        """Handle `SRclose` node."""
        return SRclose()

    def on_sr_open(self, node: SRopen) -> SRopen:
        """Handle `SRopen` node."""
        return SRopen.model_construct(
            x=node.x,
            y=node.y,
            i=node.i,
            j=node.j,
        )

    def on_ta_user_name(self, node: TA_UserName) -> TA_UserName:
        """Handle `TA_UserName` node."""
        return TA_UserName.model_construct(user_name=node.user_name, fields=node.fields)

    def on_ta_aper_function(self, node: TA_AperFunction) -> TA_AperFunction:
        """Handle `TA_AperFunction` node."""
        return TA_AperFunction.model_construct(
            function=node.function,
            fields=node.fields,
        )

    def on_ta_drill_tolerance(self, node: TA_DrillTolerance) -> TA_DrillTolerance:
        """Handle `TA_DrillTolerance` node."""
        return TA_DrillTolerance.model_construct(
            plus_tolerance=node.plus_tolerance,
            minus_tolerance=node.minus_tolerance,
        )

    def on_ta_flash_text(self, node: TA_FlashText) -> TA_FlashText:
        """Handle `TA_FlashText` node."""
        return TA_FlashText.model_construct(
            string=node.string,
            mode=node.mode,
            mirroring=node.mirroring,
            font=node.font,
            size=node.size,
            comments=node.comments,
        )

    def on_td(self, node: TD) -> TD:
        """Handle `TD` node."""
        return TD.model_construct(name=node.name)

    def on_tf_user_name(self, node: TF_UserName) -> TF_UserName:
        """Handle `TF_UserName` node."""
        return TF_UserName.model_construct(user_name=node.user_name, fields=node.fields)

    def on_tf_part(self, node: TF_Part) -> TF_Part:
        """Handle `TF_Part` node."""
        return TF_Part.model_construct(part=node.part, fields=node.fields)

    def on_tf_file_function(self, node: TF_FileFunction) -> TF_FileFunction:
        """Handle `TF_FileFunction` node."""
        return TF_FileFunction.model_construct(
            file_function=node.file_function,
            fields=node.fields,
        )

    def on_tf_file_polarity(self, node: TF_FilePolarity) -> TF_FilePolarity:
        """Handle `TF_FilePolarity` node."""
        return TF_FilePolarity.model_construct(
            polarity=node.polarity,
        )

    def on_tf_same_coordinates(self, node: TF_SameCoordinates) -> TF_SameCoordinates:
        """Handle `TF_SameCoordinates` node."""
        return TF_SameCoordinates.model_construct(
            identifier=node.identifier,
        )

    def on_tf_creation_date(self, node: TF_CreationDate) -> TF_CreationDate:
        """Handle `TF_CreationDate` node."""
        return TF_CreationDate.model_construct(
            creation_date=node.creation_date,
        )

    def on_tf_generation_software(
        self, node: TF_GenerationSoftware
    ) -> TF_GenerationSoftware:
        """Handle `TF_GenerationSoftware` node."""
        return TF_GenerationSoftware.model_construct(
            vendor=node.vendor,
            application=node.application,
            version=node.version,
        )

    def on_tf_project_id(self, node: TF_ProjectId) -> TF_ProjectId:
        """Handle `TF_ProjectId` node."""
        return TF_ProjectId.model_construct(
            name=node.name,
            guid=node.guid,
            revision=node.revision,
        )

    def on_tf_md5(self, node: TF_MD5) -> TF_MD5:
        """Handle `TF_MD5` node."""
        return TF_MD5.model_construct(md5=node.md5)

    def on_to_user_name(self, node: TO_UserName) -> TO_UserName:
        """Handle `TO_UserName` node."""
        return TO_UserName.model_construct(
            user_name=node.user_name,
            fields=node.fields,
        )

    def on_to_n(self, node: TO_N) -> TO_N:
        """Handle `TO_N` node."""
        return TO_N.model_construct(net_names=node.net_names)

    def on_to_p(self, node: TO_P) -> TO_P:
        """Handle `TO_P` node."""
        return TO_P.model_construct(
            refdes=node.refdes,
            number=node.number,
            function=node.function,
        )

    def on_to_c(self, node: TO_C) -> TO_C:
        """Handle `TO_C` node."""
        return TO_C.model_construct(refdes=node.refdes)

    def on_to_crot(self, node: TO_CRot) -> TO_CRot:
        """Handle `TO_CRot` node."""
        return TO_CRot.model_construct(angle=node.angle)

    def on_to_cmfr(self, node: TO_CMfr) -> TO_CMfr:
        """Handle `TO_CMfr` node."""
        return TO_CMfr.model_construct(manufacturer=node.manufacturer)

    def on_to_cmnp(self, node: TO_CMNP) -> TO_CMNP:
        """Handle `TO_CMNP` node."""
        return TO_CMNP.model_construct(part_number=node.part_number)

    def on_to_cval(self, node: TO_CVal) -> TO_CVal:
        """Handle `TO_CVal` node."""
        return TO_CVal.model_construct(value=node.value)

    def on_to_cmnt(self, node: TO_CMnt) -> TO_CMnt:
        """Handle `TO_CMnt` node."""
        return TO_CMnt.model_construct(mount=node.mount)

    def on_to_cftp(self, node: TO_CFtp) -> TO_CFtp:
        """Handle `TO_CFtp` node."""
        return TO_CFtp.model_construct(footprint=node.footprint)

    def on_to_cpgn(self, node: TO_CPgN) -> TO_CPgN:
        """Handle `TO_CPgN` node."""
        return TO_CPgN.model_construct(name=node.name)

    def on_to_cpgd(self, node: TO_CPgD) -> TO_CPgD:
        """Handle `TO_CPgD` node."""
        return TO_CPgD.model_construct(description=node.description)

    def on_to_chgt(self, node: TO_CHgt) -> TO_CHgt:
        """Handle `TO_CHgt` node."""
        return TO_CHgt.model_construct(height=node.height)

    def on_to_clbn(self, node: TO_CLbN) -> TO_CLbN:
        """Handle `TO_CLbN` node."""
        return TO_CLbN.model_construct(name=node.name)

    def on_to_clbd(self, node: TO_CLbD) -> TO_CLbD:
        """Handle `TO_CLbD` node."""
        return TO_CLbD.model_construct(description=node.description)

    def on_to_csup(self, node: TO_CSup) -> TO_CSup:
        """Handle `TO_CSup` node."""
        return TO_CSup.model_construct(
            supplier=node.supplier,
            supplier_part=node.supplier_part,
            other_suppliers=node.other_suppliers,
        )

    def on_d01(self, node: D01) -> D01:
        """Handle `D01` node."""
        return D01.model_construct(
            x=node.x,
            y=node.y,
            i=node.i,
            j=node.j,
        )

    def on_d02(self, node: D02) -> D02:
        """Handle `D02` node."""
        return D02.model_construct(
            x=node.x,
            y=node.y,
        )

    def on_d03(self, node: D03) -> D03:
        """Handle `D03` node."""
        return D03.model_construct(
            x=node.x,
            y=node.y,
        )

    def on_dnn(self, node: Dnn) -> Dnn:
        """Handle `Dnn` node."""
        return Dnn.model_construct(
            aperture_id=node.aperture_id,
        )

    def on_g01(self, node: G01) -> G01:  # noqa: ARG002
        """Handle `G01` node."""
        return G01.model_construct()

    def on_g02(self, node: G02) -> G02:  # noqa: ARG002
        """Handle `G02` node."""
        return G02.model_construct()

    def on_g03(self, node: G03) -> G03:  # noqa: ARG002
        """Handle `G03` node."""
        return G03.model_construct()

    def on_g04(self, node: G04) -> G04:  # noqa: ARG002
        """Handle `G04` node."""
        return G04.model_construct()

    def on_g36(self, node: G36) -> G36:  # noqa: ARG002
        """Handle `G36` node."""
        return G36.model_construct()

    def on_g37(self, node: G37) -> G37:  # noqa: ARG002
        """Handle `G37` node."""
        return G37.model_construct()

    def on_g54(self, node: G54) -> G54:  # noqa: ARG002
        """Handle `G54` node."""
        return G54.model_construct()

    def on_g55(self, node: G55) -> G55:  # noqa: ARG002
        """Handle `G55` node."""
        return G55.model_construct()

    def on_g70(self, node: G70) -> G70:  # noqa: ARG002
        """Handle `G70` node."""
        return G70.model_construct()

    def on_g71(self, node: G71) -> G71:  # noqa: ARG002
        """Handle `G71` node."""
        return G71.model_construct()

    def on_g74(self, node: G74) -> G74:  # noqa: ARG002
        """Handle `G74` node."""
        return G74.model_construct()

    def on_g75(self, node: G75) -> G75:  # noqa: ARG002
        """Handle `G75` node."""
        return G75.model_construct()

    def on_g90(self, node: G90) -> G90:  # noqa: ARG002
        """Handle `G90` node."""
        return G90.model_construct()

    def on_g91(self, node: G91) -> G91:  # noqa: ARG002
        """Handle `G91` node."""
        return G91.model_construct()

    def on_lm(self, node: LM) -> LM:
        """Handle `LM` node."""
        return LM.model_construct(
            mirroring=node.mirroring,
        )

    def on_ln(self, node: LN) -> LN:
        """Handle `LN` node."""
        return LN.model_construct(
            name=node.name,
        )

    def on_lp(self, node: LP) -> LP:
        """Handle `LP` node."""
        return LP.model_construct(
            polarity=node.polarity,
        )

    def on_lr(self, node: LR) -> LR:
        """Handle `LR` node."""
        return LR.model_construct(
            rotation=node.rotation,
        )

    def on_ls(self, node: LS) -> LS:
        """Handle `LS` node."""
        return LS.model_construct(
            scale=node.scale,
        )

    def on_m00(self, node: M00) -> M00:  # noqa: ARG002
        """Handle `M00` node."""
        return M00.model_construct()

    def on_m01(self, node: M01) -> M01:  # noqa: ARG002
        """Handle `M01` node."""
        return M01.model_construct()

    def on_m02(self, node: M02) -> M02:  # noqa: ARG002
        """Handle `M02` node."""
        return M02.model_construct()

    def on_add(self, node: Add) -> Add:
        """Handle `Add` node."""
        head = node.head.visit(self)
        tail = [operand.visit(self) for operand in node.tail]
        return Add.model_construct(head=head, tail=tail)

    def on_sub(self, node: Sub) -> Sub:
        """Handle `Sub` node."""
        head = node.head.visit(self)
        tail = [operand.visit(self) for operand in node.tail]
        return Sub.model_construct(head=head, tail=tail)

    def on_mul(self, node: Mul) -> Mul:
        """Handle `Mul` node."""
        head = node.head.visit(self)
        tail = [operand.visit(self) for operand in node.tail]
        return Mul.model_construct(head=head, tail=tail)

    def on_div(self, node: Div) -> Div:
        """Handle `Div` node."""
        head = node.head.visit(self)
        tail = [operand.visit(self) for operand in node.tail]
        return Div.model_construct(head=head, tail=tail)

    def on_neg(self, node: Neg) -> Neg:
        """Handle `Neg` node."""
        return Neg.model_construct(operand=node.operand.visit(self))

    def on_pos(self, node: Pos) -> Pos:
        """Handle `Pos` node."""
        return Pos.model_construct(operand=node.operand.visit(self))

    def on_assignment(self, node: Assignment) -> Assignment:
        """Handle `Assignment` node."""
        variable = node.variable.visit(self)
        expression = node.expression.visit(self)
        return Assignment.model_construct(variable=variable, expression=expression)

    def on_constant(self, node: Constant) -> Constant:
        """Handle `Constant` node."""
        return Constant.model_construct(constant=node.constant)

    def on_parenthesis(self, node: Parenthesis) -> Parenthesis:
        """Handle `Parenthesis` node."""
        return Parenthesis.model_construct(inner=node.inner.visit(self))

    def on_point(self, node: Point) -> Point:
        """Handle `Point` node."""
        return Point.model_construct(x=node.x.visit(self), y=node.y.visit(self))

    def on_variable(self, node: Variable) -> Variable:
        """Handle `Variable` node."""
        return Variable.model_construct(variable=node.variable)

    def on_coordinate_x(self, node: CoordinateX) -> CoordinateX:
        """Handle `Coordinate` node."""
        return CoordinateX.model_construct(value=node.value)

    def on_coordinate_y(self, node: CoordinateY) -> CoordinateY:
        """Handle `Coordinate` node."""
        return CoordinateY.model_construct(value=node.value)

    def on_coordinate_i(self, node: CoordinateI) -> CoordinateI:
        """Handle `Coordinate` node."""
        return CoordinateI.model_construct(value=node.value)

    def on_coordinate_j(self, node: CoordinateJ) -> CoordinateJ:
        """Handle `Coordinate` node."""
        return CoordinateJ.model_construct(value=node.value)

    def on_code_0(self, node: Code0) -> Code0:
        """Handle `Code0` node."""
        return Code0.model_construct(string=node.string)

    def on_code_1(self, node: Code1) -> Code1:
        """Handle `Code1` node."""
        return Code1.model_construct(
            exposure=node.exposure.visit(self),
            diameter=node.diameter.visit(self),
            center_x=node.center_x.visit(self),
            center_y=node.center_y.visit(self),
            rotation=node.rotation.visit(self) if node.rotation is not None else None,
        )

    def on_code_2(self, node: Code2) -> Code2:
        """Handle `Code2` node."""
        return Code2.model_construct(
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
        return Code4.model_construct(
            exposure=node.exposure.visit(self),
            number_of_points=node.number_of_points.visit(self),
            start_x=node.start_x.visit(self),
            start_y=node.start_y.visit(self),
            points=[point.visit(self) for point in node.points],
            rotation=node.rotation.visit(self),
        )

    def on_code_5(self, node: Code5) -> Code5:
        """Handle `Code5` node."""
        return Code5.model_construct(
            exposure=node.exposure.visit(self),
            number_of_vertices=node.number_of_vertices.visit(self),
            center_x=node.center_x.visit(self),
            center_y=node.center_y.visit(self),
            diameter=node.diameter.visit(self),
            rotation=node.rotation.visit(self),
        )

    def on_code_6(self, node: Code6) -> Code6:
        """Handle `Code6` node."""
        return Code6.model_construct(
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
        return Code7.model_construct(
            center_x=node.center_x.visit(self),
            center_y=node.center_y.visit(self),
            outer_diameter=node.outer_diameter.visit(self),
            inner_diameter=node.inner_diameter.visit(self),
            gap_thickness=node.gap_thickness.visit(self),
            rotation=node.rotation.visit(self),
        )

    def on_code_20(self, node: Code20) -> Code20:
        """Handle `Code20` node."""
        return Code20.model_construct(
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
        return Code21.model_construct(
            exposure=node.exposure.visit(self),
            width=node.width.visit(self),
            height=node.height.visit(self),
            center_x=node.center_x.visit(self),
            center_y=node.center_y.visit(self),
            rotation=node.rotation.visit(self),
        )

    def on_code_22(self, node: Code22) -> Code22:
        """Handle `Code22` node."""
        return Code22.model_construct(
            exposure=node.exposure.visit(self),
            width=node.width.visit(self),
            height=node.height.visit(self),
            x_lower_left=node.x_lower_left.visit(self),
            y_lower_left=node.y_lower_left.visit(self),
            rotation=node.rotation.visit(self),
        )

    def on_as(self, node: AS) -> AS:
        """Handle `AS` node."""
        return AS.model_construct(
            correspondence=node.correspondence,
        )

    def on_fs(self, node: FS) -> FS:
        """Handle `FS` node."""
        return FS.model_construct(
            zeros=node.zeros,
            coordinate_mode=node.coordinate_mode,
            x_integral=node.x_integral,
            x_decimal=node.x_decimal,
            y_integral=node.y_integral,
            y_decimal=node.y_decimal,
        )

    def on_in(self, node: IN) -> IN:
        """Handle `IN` node."""
        return IN.model_construct(name=node.name)

    def on_ip(self, node: IP) -> IP:
        """Handle `IP` node."""
        return IP.model_construct(
            polarity=node.polarity,
        )

    def on_ir(self, node: IR) -> IR:
        """Handle `IR` node."""
        return IR.model_construct(rotation_degrees=node.rotation_degrees)

    def on_mi(self, node: MI) -> MI:
        """Handle `MI` node."""
        return MI.model_construct(
            a_mirroring=node.a_mirroring, b_mirroring=node.b_mirroring
        )

    def on_mo(self, node: MO) -> MO:
        """Handle `MO` node."""
        return MO.model_construct(
            mode=node.mode,
        )

    def on_of(self, node: OF) -> OF:
        """Handle `OF` node."""
        return OF.model_construct(
            a_offset=node.a_offset,
            b_offset=node.b_offset,
        )

    def on_sf(self, node: SF) -> SF:
        """Handle `SF` node."""
        return SF.model_construct(
            a_scale=node.a_scale,
            b_scale=node.b_scale,
        )

    def on_file(self, node: File) -> File:
        """Handle `File` node."""
        nodes = []
        try:
            for command in node.nodes:
                try:
                    nodes.append(command.visit(self))

                except DeepDiscardNode:  # noqa: PERF203
                    # Discard node
                    pass

                except ShallowDiscardNode:
                    # Discard node
                    pass

                except Exception as e:
                    if self.on_exception(command, e):
                        raise
        finally:
            self.on_end_of_file(node)

        return node

    def on_invalid(self, node: Invalid) -> Invalid:
        """Handle invalid node."""
        return Invalid(string=node.string)

    def optimize(self, node: File) -> File:
        """Optimize AST."""
        self._original = node
        try:
            result = node.visit(self)
        finally:
            self._original = None

        return result
