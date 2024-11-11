from __future__ import annotations

import datetime
from typing import Dict, Type
from unittest import mock

import pytest
import tzlocal

from pygerber.gerber.ast.ast_visitor import AstVisitor
from pygerber.gerber.ast.nodes.aperture.AB_close import ABclose
from pygerber.gerber.ast.nodes.aperture.AB_open import ABopen
from pygerber.gerber.ast.nodes.aperture.ADC import ADC
from pygerber.gerber.ast.nodes.aperture.ADmacro import ADmacro
from pygerber.gerber.ast.nodes.aperture.ADO import ADO
from pygerber.gerber.ast.nodes.aperture.ADP import ADP
from pygerber.gerber.ast.nodes.aperture.ADR import ADR
from pygerber.gerber.ast.nodes.aperture.AM_close import AMclose
from pygerber.gerber.ast.nodes.aperture.AM_open import AMopen
from pygerber.gerber.ast.nodes.aperture.SR_close import SRclose
from pygerber.gerber.ast.nodes.aperture.SR_open import SRopen
from pygerber.gerber.ast.nodes.attribute.TA import (
    AperFunction,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
)
from pygerber.gerber.ast.nodes.attribute.TD import TD
from pygerber.gerber.ast.nodes.attribute.TF import (
    TF_MD5,
    FileFunction,
    Part,
    TF_CreationDate,
    TF_FileFunction,
    TF_FilePolarity,
    TF_GenerationSoftware,
    TF_Part,
    TF_ProjectId,
    TF_SameCoordinates,
    TF_UserName,
)
from pygerber.gerber.ast.nodes.attribute.TO import (
    TO_C,
    TO_CMNP,
    TO_N,
    TO_P,
    Mount,
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
from pygerber.gerber.ast.nodes.base import Node
from pygerber.gerber.ast.nodes.d_codes.D01 import D01
from pygerber.gerber.ast.nodes.d_codes.D02 import D02
from pygerber.gerber.ast.nodes.d_codes.D03 import D03
from pygerber.gerber.ast.nodes.d_codes.Dnn import Dnn
from pygerber.gerber.ast.nodes.enums import CoordinateNotation, ImagePolarity, Zeros
from pygerber.gerber.ast.nodes.file import File
from pygerber.gerber.ast.nodes.g_codes.G01 import G01
from pygerber.gerber.ast.nodes.g_codes.G02 import G02
from pygerber.gerber.ast.nodes.g_codes.G03 import G03
from pygerber.gerber.ast.nodes.g_codes.G04 import G04
from pygerber.gerber.ast.nodes.g_codes.G36 import G36
from pygerber.gerber.ast.nodes.g_codes.G37 import G37
from pygerber.gerber.ast.nodes.g_codes.G54 import G54
from pygerber.gerber.ast.nodes.g_codes.G55 import G55
from pygerber.gerber.ast.nodes.g_codes.G70 import G70
from pygerber.gerber.ast.nodes.g_codes.G71 import G71
from pygerber.gerber.ast.nodes.g_codes.G74 import G74
from pygerber.gerber.ast.nodes.g_codes.G75 import G75
from pygerber.gerber.ast.nodes.g_codes.G90 import G90
from pygerber.gerber.ast.nodes.g_codes.G91 import G91
from pygerber.gerber.ast.nodes.load.LM import LM, Mirroring
from pygerber.gerber.ast.nodes.load.LN import LN
from pygerber.gerber.ast.nodes.load.LP import LP, Polarity
from pygerber.gerber.ast.nodes.load.LR import LR
from pygerber.gerber.ast.nodes.load.LS import LS
from pygerber.gerber.ast.nodes.m_codes.M00 import M00
from pygerber.gerber.ast.nodes.m_codes.M01 import M01
from pygerber.gerber.ast.nodes.m_codes.M02 import M02
from pygerber.gerber.ast.nodes.math.assignment import Assignment
from pygerber.gerber.ast.nodes.math.constant import Constant
from pygerber.gerber.ast.nodes.math.operators.binary.add import Add
from pygerber.gerber.ast.nodes.math.operators.binary.div import Div
from pygerber.gerber.ast.nodes.math.operators.binary.mul import Mul
from pygerber.gerber.ast.nodes.math.operators.binary.sub import Sub
from pygerber.gerber.ast.nodes.math.operators.unary.neg import Neg
from pygerber.gerber.ast.nodes.math.operators.unary.pos import Pos
from pygerber.gerber.ast.nodes.math.point import Point
from pygerber.gerber.ast.nodes.math.variable import Variable
from pygerber.gerber.ast.nodes.other.coordinate import (
    CoordinateI,
    CoordinateJ,
    CoordinateX,
    CoordinateY,
)
from pygerber.gerber.ast.nodes.primitives.code_0 import Code0
from pygerber.gerber.ast.nodes.primitives.code_1 import Code1
from pygerber.gerber.ast.nodes.primitives.code_2 import Code2
from pygerber.gerber.ast.nodes.primitives.code_4 import Code4
from pygerber.gerber.ast.nodes.primitives.code_5 import Code5
from pygerber.gerber.ast.nodes.primitives.code_6 import Code6
from pygerber.gerber.ast.nodes.primitives.code_7 import Code7
from pygerber.gerber.ast.nodes.primitives.code_20 import Code20
from pygerber.gerber.ast.nodes.primitives.code_21 import Code21
from pygerber.gerber.ast.nodes.primitives.code_22 import Code22
from pygerber.gerber.ast.nodes.properties.AS import AS, AxisCorrespondence
from pygerber.gerber.ast.nodes.properties.FS import FS
from pygerber.gerber.ast.nodes.properties.IN import IN
from pygerber.gerber.ast.nodes.properties.IP import IP
from pygerber.gerber.ast.nodes.properties.IR import IR
from pygerber.gerber.ast.nodes.properties.MI import MI
from pygerber.gerber.ast.nodes.properties.MO import MO, UnitMode
from pygerber.gerber.ast.nodes.properties.OF import OF
from pygerber.gerber.ast.nodes.properties.SF import SF
from pygerber.gerber.ast.nodes.types import ApertureIdStr, PackedCoordinateStr

NODE_SAMPLES: Dict[Type[Node], Node] = {
    ABclose: ABclose(),
    ABopen: ABopen(aperture_id=ApertureIdStr("D11")),
    ADC: ADC(
        aperture_id=ApertureIdStr("D11"),
        diameter=0.1,
        hole_diameter=0.05,
    ),
    ADmacro: ADmacro(
        aperture_id=ApertureIdStr("D11"),
        name="macro",
        params=[1, 2],
    ),
    ADO: ADO(
        aperture_id=ApertureIdStr("D11"),
        width=0.1,
        height=0.05,
        hole_diameter=0.05,
    ),
    ADR: ADR(
        aperture_id=ApertureIdStr("D11"),
        width=0.1,
        height=0.05,
        hole_diameter=0.05,
    ),
    ADP: ADP(
        aperture_id=ApertureIdStr("D11"),
        outer_diameter=0.1,
        vertices=4,
        rotation=0.1,
        hole_diameter=0.05,
    ),
    AMclose: AMclose(),
    AMopen: AMopen(name="macro"),
    SRclose: SRclose(),
    SRopen: SRopen(x="1", y="2", i="3", j="4"),
    TA_UserName: TA_UserName(user_name="user"),
    TA_AperFunction: TA_AperFunction(function=AperFunction.ViaDrill),
    TA_DrillTolerance: TA_DrillTolerance(plus_tolerance=0.1, minus_tolerance=0.05),
    TA_FlashText: TA_FlashText(
        string="Hello World",
        mode="B",
        mirroring="R",
        font=None,
        size=None,
        comments=[],
    ),
    TD: TD(name="name"),
    TF_UserName: TF_UserName(user_name="user"),
    TF_Part: TF_Part(part=Part.Single),
    TF_FileFunction: TF_FileFunction(file_function=FileFunction.Copper),
    TF_FilePolarity: TF_FilePolarity(polarity="Positive"),
    TF_SameCoordinates: TF_SameCoordinates(
        identifier="CA9C4AC4-C4BE-41B9-9754-440A126A42FF"
    ),
    TF_CreationDate: TF_CreationDate(
        creation_date=datetime.datetime.now(tz=tzlocal.get_localzone()),
    ),
    TF_GenerationSoftware: TF_GenerationSoftware(
        vendor="vendor",
        application="application",
        version="version",
    ),
    TF_ProjectId: TF_ProjectId(
        name="name",
        guid="guid",
        revision="revision",
    ),
    TF_MD5: TF_MD5(md5="0" * 32),
    TO_UserName: TO_UserName(user_name="user"),
    TO_N: TO_N(net_names=["net"]),
    TO_P: TO_P(refdes="refdes", number="number"),
    TO_C: TO_C(refdes="refdes"),
    TO_CRot: TO_CRot(angle=0.1),
    TO_CMfr: TO_CMfr(manufacturer="manufacturer"),
    TO_CMNP: TO_CMNP(part_number="part_number"),
    TO_CVal: TO_CVal(value="value"),
    TO_CMnt: TO_CMnt(mount=Mount.SMD),
    TO_CFtp: TO_CFtp(footprint="footprint"),
    TO_CPgN: TO_CPgN(name="name"),
    TO_CPgD: TO_CPgD(description="description"),
    TO_CHgt: TO_CHgt(height=0.1),
    TO_CLbN: TO_CLbN(name="name"),
    TO_CLbD: TO_CLbD(description="description"),
    TO_CSup: TO_CSup(supplier="supplier", supplier_part="supplier_part"),
    D01: D01(x=None, y=None, i=None, j=None),
    D02: D02(
        x=CoordinateX(value=PackedCoordinateStr("1")),
        y=CoordinateY(value=PackedCoordinateStr("2")),
    ),
    D03: D03(
        x=CoordinateX(value=PackedCoordinateStr("1")),
        y=CoordinateY(value=PackedCoordinateStr("2")),
    ),
    Dnn: Dnn(aperture_id=ApertureIdStr("D11")),
    G01: G01(),
    G02: G02(),
    G03: G03(),
    G04: G04(string="comment"),
    G36: G36(),
    G37: G37(),
    G54: G54(),
    G55: G55(),
    G70: G70(),
    G71: G71(),
    G74: G74(),
    G75: G75(),
    G90: G90(),
    G91: G91(),
    LM: LM(mirroring=Mirroring.XY),
    LN: LN(name="name"),
    LP: LP(polarity=Polarity.Clear),
    LR: LR(rotation=0.1),
    LS: LS(scale=0.1),
    M00: M00(),
    M01: M01(),
    M02: M02(),
    Add: Add(
        head=Constant(constant=1),
        tail=[
            Constant(constant=2),
        ],
    ),
    Div: Div(
        head=Constant(constant=1),
        tail=[
            Constant(constant=2),
        ],
    ),
    Mul: Mul(
        head=Constant(constant=1),
        tail=[
            Constant(constant=2),
        ],
    ),
    Sub: Sub(
        head=Constant(constant=1),
        tail=[
            Constant(constant=2),
        ],
    ),
    Neg: Neg(
        operand=Constant(constant=2),
    ),
    Pos: Pos(
        operand=Constant(constant=2),
    ),
    Assignment: Assignment(
        variable=Variable(variable="$1"),
        expression=Constant(constant=1),
    ),
    Constant: Constant(constant=2),
    Point: Point(
        x=Constant(constant=1),
        y=Constant(constant=2),
    ),
    Variable: Variable(variable="$1"),
    CoordinateX: CoordinateX(value=PackedCoordinateStr("1")),
    CoordinateY: CoordinateY(value=PackedCoordinateStr("1")),
    CoordinateI: CoordinateI(value=PackedCoordinateStr("1")),
    CoordinateJ: CoordinateJ(value=PackedCoordinateStr("1")),
    Code0: Code0(string="string"),
    Code1: Code1(
        exposure=Constant(constant=1),
        diameter=Constant(constant=2),
        center_x=Constant(constant=3),
        center_y=Constant(constant=4),
    ),
    Code2: Code2(
        exposure=Constant(constant=1),
        width=Constant(constant=2),
        start_x=Constant(constant=3),
        start_y=Constant(constant=4),
        end_x=Constant(constant=5),
        end_y=Constant(constant=6),
        rotation=Constant(constant=7),
    ),
    Code4: Code4(
        exposure=Constant(constant=1),
        number_of_points=Constant(constant=2),
        start_x=Constant(constant=3),
        start_y=Constant(constant=4),
        points=[
            Point(
                x=Constant(constant=1),
                y=Constant(constant=2),
            )
        ],
        rotation=Constant(constant=5),
    ),
    Code5: Code5(
        exposure=Constant(constant=1),
        number_of_vertices=Constant(constant=2),
        center_x=Constant(constant=3),
        center_y=Constant(constant=4),
        diameter=Constant(constant=5),
        rotation=Constant(constant=6),
    ),
    Code6: Code6(
        center_x=Constant(constant=3),
        center_y=Constant(constant=4),
        outer_diameter=Constant(constant=5),
        ring_thickness=Constant(constant=1),
        gap_between_rings=Constant(constant=1),
        max_ring_count=Constant(constant=4),
        crosshair_thickness=Constant(constant=4),
        crosshair_length=Constant(constant=4),
        rotation=Constant(constant=6),
    ),
    Code7: Code7(
        center_x=Constant(constant=3),
        center_y=Constant(constant=4),
        outer_diameter=Constant(constant=5),
        inner_diameter=Constant(constant=1),
        gap_thickness=Constant(constant=1),
        rotation=Constant(constant=6),
    ),
    Code20: Code20(
        exposure=Constant(constant=1),
        width=Constant(constant=2),
        start_x=Constant(constant=3),
        start_y=Constant(constant=4),
        end_x=Constant(constant=5),
        end_y=Constant(constant=6),
        rotation=Constant(constant=7),
    ),
    Code21: Code21(
        exposure=Constant(constant=1),
        width=Constant(constant=2),
        height=Constant(constant=3),
        center_x=Constant(constant=4),
        center_y=Constant(constant=5),
        rotation=Constant(constant=6),
    ),
    Code22: Code22(
        exposure=Constant(constant=1),
        width=Constant(constant=2),
        height=Constant(constant=3),
        x_lower_left=Constant(constant=4),
        y_lower_left=Constant(constant=5),
        rotation=Constant(constant=6),
    ),
    AS: AS(correspondence=AxisCorrespondence.AX_BY),
    FS: FS(
        zeros=Zeros.SKIP_LEADING,
        coordinate_mode=CoordinateNotation.ABSOLUTE,
        x_integral=2,
        x_decimal=3,
        y_integral=4,
        y_decimal=5,
    ),
    IN: IN(name="name"),
    IP: IP(polarity=ImagePolarity.POSITIVE),
    IR: IR(rotation_degrees=90),
    MI: MI(a_mirroring=0, b_mirroring=1),
    MO: MO(mode=UnitMode.METRIC),
    OF: OF(a_offset=1, b_offset=2),
    SF: SF(a_scale=1.0, b_scale=1.0),
    File: File(nodes=[]),
}


class TestAstVisitor:
    @pytest.mark.parametrize(("_type", "instance"), NODE_SAMPLES.items())
    def test_visit_node(self, _type: Type[Node], instance: Node) -> None:  # noqa: PT019
        callback_mock = mock.Mock()
        visitor = AstVisitor()
        setattr(
            visitor,
            instance.get_visitor_callback_function(visitor).__name__,
            callback_mock,
        )

        instance.visit(visitor)

        # Assert that the callback was properly called
        callback_mock.assert_called_once_with(instance)

    def test_iter_all(self) -> None:
        """Simply call visit method on all nodes to ensure default implementations work."""
        visitor = AstVisitor()
        for node in NODE_SAMPLES.values():
            node.visit(visitor)
