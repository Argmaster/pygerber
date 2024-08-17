from __future__ import annotations

import datetime
from typing import Dict, Type
from unittest import mock

import pytest
import tzlocal

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
    AperFunction,
    TA_AperFunction,
    TA_DrillTolerance,
    TA_FlashText,
    TA_UserName,
)
from pygerber.gerberx3.ast.nodes.attribute.TD import TD
from pygerber.gerberx3.ast.nodes.attribute.TF import (
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
from pygerber.gerberx3.ast.nodes.attribute.TO import (
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
from pygerber.gerberx3.ast.nodes.base import Node
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
from pygerber.gerberx3.ast.nodes.load.LM import LM, Mirroring
from pygerber.gerberx3.ast.nodes.load.LN import LN
from pygerber.gerberx3.ast.nodes.load.LP import LP, Polarity
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
from pygerber.gerberx3.ast.nodes.properties.AS import AS, AxisCorrespondence
from pygerber.gerberx3.ast.nodes.properties.FS import FS
from pygerber.gerberx3.ast.nodes.properties.IN import IN
from pygerber.gerberx3.ast.nodes.properties.IP import IP
from pygerber.gerberx3.ast.nodes.properties.IR import IR
from pygerber.gerberx3.ast.nodes.properties.MI import MI
from pygerber.gerberx3.ast.nodes.properties.MO import MO, UnitMode
from pygerber.gerberx3.ast.nodes.properties.OF import OF
from pygerber.gerberx3.ast.nodes.properties.SF import SF
from pygerber.gerberx3.ast.visitor import AstVisitor

NODE_SAMPLES: Dict[Type[Node], Node] = {
    ABclose: ABclose(source="", location=0),
    ABopen: ABopen(source="", location=0, aperture_identifier="D11"),
    ADC: ADC(
        source="",
        location=0,
        aperture_identifier="D11",
        diameter="0.1",
        hole_diameter="0.05",
    ),
    ADmacro: ADmacro(
        source="",
        location=0,
        aperture_identifier="D11",
        name="macro",
        params=["1", "2"],
    ),
    ADO: ADO(
        source="",
        location=0,
        aperture_identifier="D11",
        width="0.1",
        height="0.05",
        hole_diameter="0.05",
    ),
    ADR: ADR(
        source="",
        location=0,
        aperture_identifier="D11",
        width="0.1",
        height="0.05",
        hole_diameter="0.05",
    ),
    ADP: ADP(
        source="",
        location=0,
        aperture_identifier="D11",
        outer_diameter="0.1",
        vertices="4",
        rotation="0.1",
        hole_diameter="0.05",
    ),
    AMclose: AMclose(source="", location=0),
    AMopen: AMopen(source="", location=0, name="macro"),
    SRclose: SRclose(source="", location=0),
    SRopen: SRopen(source="", location=0, x="1", y="2", i="3", j="4"),
    TA_UserName: TA_UserName(source="", location=0, user_name="user"),
    TA_AperFunction: TA_AperFunction(
        source="", location=0, function=AperFunction.ViaDrill
    ),
    TA_DrillTolerance: TA_DrillTolerance(
        source="", location=0, plus_tolerance=0.1, minus_tolerance=0.05
    ),
    TA_FlashText: TA_FlashText(
        source="",
        location=0,
        string="Hello World",
        mode="B",
        mirroring="R",
        font=None,
        size=None,
        comments=[],
    ),
    TD: TD(source="", location=0, name="name"),
    TF_UserName: TF_UserName(source="", location=0, user_name="user"),
    TF_Part: TF_Part(source="", location=0, part=Part.Single),
    TF_FileFunction: TF_FileFunction(
        source="", location=0, file_function=FileFunction.Copper
    ),
    TF_FilePolarity: TF_FilePolarity(source="", location=0, polarity="Positive"),
    TF_SameCoordinates: TF_SameCoordinates(
        source="", location=0, identifier="CA9C4AC4-C4BE-41B9-9754-440A126A42FF"
    ),
    TF_CreationDate: TF_CreationDate(
        source="",
        location=0,
        creation_date=datetime.datetime.now(tz=tzlocal.get_localzone()),
    ),
    TF_GenerationSoftware: TF_GenerationSoftware(
        source="",
        location=0,
        vendor="vendor",
        application="application",
        version="version",
    ),
    TF_ProjectId: TF_ProjectId(
        source="",
        location=0,
        name="name",
        guid="guid",
        revision="revision",
    ),
    TF_MD5: TF_MD5(source="", location=0, md5="0" * 32),
    TO_UserName: TO_UserName(source="", location=0, user_name="user"),
    TO_N: TO_N(source="", location=0, net_names=["net"]),
    TO_P: TO_P(source="", location=0, refdes="refdes", number="number"),
    TO_C: TO_C(source="", location=0, refdes="refdes"),
    TO_CRot: TO_CRot(source="", location=0, angle=0.1),
    TO_CMfr: TO_CMfr(source="", location=0, manufacturer="manufacturer"),
    TO_CMNP: TO_CMNP(source="", location=0, part_number="part_number"),
    TO_CVal: TO_CVal(source="", location=0, value="value"),
    TO_CMnt: TO_CMnt(source="", location=0, mount=Mount.SMD),
    TO_CFtp: TO_CFtp(source="", location=0, footprint="footprint"),
    TO_CPgN: TO_CPgN(source="", location=0, name="name"),
    TO_CPgD: TO_CPgD(source="", location=0, description="description"),
    TO_CHgt: TO_CHgt(source="", location=0, height=0.1),
    TO_CLbN: TO_CLbN(source="", location=0, name="name"),
    TO_CLbD: TO_CLbD(source="", location=0, description="description"),
    TO_CSup: TO_CSup(
        source="", location=0, supplier="supplier", supplier_part="supplier_part"
    ),
    D01: D01(source="", location=0, x=None, y=None, i=None, j=None),
    D02: D02(
        source="",
        location=0,
        x=CoordinateX(source="", location=0, value="1"),
        y=CoordinateY(source="", location=0, value="2"),
    ),
    D03: D03(
        source="",
        location=0,
        x=CoordinateX(source="", location=0, value="1"),
        y=CoordinateY(source="", location=0, value="2"),
    ),
    Dnn: Dnn(source="", location=0, value="D11"),
    G01: G01(source="", location=0),
    G02: G02(source="", location=0),
    G03: G03(source="", location=0),
    G04: G04(source="", location=0, string="comment"),
    G36: G36(source="", location=0),
    G37: G37(source="", location=0),
    G54: G54(source="", location=0, dnn=Dnn(source="", location=0, value="D11")),
    G55: G55(source="", location=0, flash=D03(source="", location=0)),
    G70: G70(source="", location=0),
    G71: G71(source="", location=0),
    G74: G74(source="", location=0),
    G75: G75(source="", location=0),
    G90: G90(source="", location=0),
    G91: G91(source="", location=0),
    LM: LM(source="", location=0, mirroring=Mirroring.XY),
    LN: LN(source="", location=0, name="name"),
    LP: LP(source="", location=0, polarity=Polarity.Clear),
    LR: LR(source="", location=0, rotation=0.1),
    LS: LS(source="", location=0, scale=0.1),
    M00: M00(source="", location=0),
    M01: M01(source="", location=0),
    M02: M02(source="", location=0),
    Add: Add(
        source="",
        location=0,
        operands=[
            Constant(source="", location=0, constant="1"),
            Constant(source="", location=0, constant="2"),
        ],
    ),
    Div: Div(
        source="",
        location=0,
        operands=[
            Constant(source="", location=0, constant="1"),
            Constant(source="", location=0, constant="2"),
        ],
    ),
    Mul: Mul(
        source="",
        location=0,
        operands=[
            Constant(source="", location=0, constant="1"),
            Constant(source="", location=0, constant="2"),
        ],
    ),
    Sub: Sub(
        source="",
        location=0,
        operands=[
            Constant(source="", location=0, constant="1"),
            Constant(source="", location=0, constant="2"),
        ],
    ),
    Neg: Neg(
        source="",
        location=0,
        operand=Constant(source="", location=0, constant="2"),
    ),
    Pos: Pos(
        source="",
        location=0,
        operand=Constant(source="", location=0, constant="2"),
    ),
    Assignment: Assignment(
        source="",
        location=0,
        variable=Variable(source="", location=0, variable="$1"),
        expression=Constant(source="", location=0, constant="1"),
    ),
    Constant: Constant(source="", location=0, constant="2"),
    Point: Point(
        source="",
        location=0,
        x=Constant(source="", location=0, constant="1"),
        y=Constant(source="", location=0, constant="2"),
    ),
    Variable: Variable(source="", location=0, variable="$1"),
    CoordinateX: CoordinateX(source="", location=0, value="1"),
    CoordinateY: CoordinateY(source="", location=0, value="1"),
    CoordinateI: CoordinateI(source="", location=0, value="1"),
    CoordinateJ: CoordinateJ(source="", location=0, value="1"),
    Code0: Code0(source="", location=0, string="string"),
    Code1: Code1(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        diameter=Constant(source="", location=0, constant="2"),
        center_x=Constant(source="", location=0, constant="3"),
        center_y=Constant(source="", location=0, constant="4"),
    ),
    Code2: Code2(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        width=Constant(source="", location=0, constant="2"),
        start_x=Constant(source="", location=0, constant="3"),
        start_y=Constant(source="", location=0, constant="4"),
        end_x=Constant(source="", location=0, constant="5"),
        end_y=Constant(source="", location=0, constant="6"),
        rotation=Constant(source="", location=0, constant="7"),
    ),
    Code4: Code4(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        number_of_points=Constant(source="", location=0, constant="2"),
        start_x=Constant(source="", location=0, constant="3"),
        start_y=Constant(source="", location=0, constant="4"),
        points=[
            Point(
                source="",
                location=0,
                x=Constant(source="", location=0, constant="1"),
                y=Constant(source="", location=0, constant="2"),
            )
        ],
        rotation=Constant(source="", location=0, constant="5"),
    ),
    Code5: Code5(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        number_of_vertices=Constant(source="", location=0, constant="2"),
        center_x=Constant(source="", location=0, constant="3"),
        center_y=Constant(source="", location=0, constant="4"),
        diameter=Constant(source="", location=0, constant="5"),
        rotation=Constant(source="", location=0, constant="6"),
    ),
    Code6: Code6(
        source="",
        location=0,
        center_x=Constant(source="", location=0, constant="3"),
        center_y=Constant(source="", location=0, constant="4"),
        outer_diameter=Constant(source="", location=0, constant="5"),
        ring_thickness=Constant(source="", location=0, constant="1"),
        gap_between_rings=Constant(source="", location=0, constant="1"),
        max_ring_count=Constant(source="", location=0, constant="4"),
        crosshair_thickness=Constant(source="", location=0, constant="4"),
        crosshair_length=Constant(source="", location=0, constant="4"),
        rotation=Constant(source="", location=0, constant="6"),
    ),
    Code7: Code7(
        source="",
        location=0,
        center_x=Constant(source="", location=0, constant="3"),
        center_y=Constant(source="", location=0, constant="4"),
        outer_diameter=Constant(source="", location=0, constant="5"),
        inner_diameter=Constant(source="", location=0, constant="1"),
        gap_thickness=Constant(source="", location=0, constant="1"),
        rotation=Constant(source="", location=0, constant="6"),
    ),
    Code20: Code20(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        width=Constant(source="", location=0, constant="2"),
        start_x=Constant(source="", location=0, constant="3"),
        start_y=Constant(source="", location=0, constant="4"),
        end_x=Constant(source="", location=0, constant="5"),
        end_y=Constant(source="", location=0, constant="6"),
        rotation=Constant(source="", location=0, constant="7"),
    ),
    Code21: Code21(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        width=Constant(source="", location=0, constant="2"),
        height=Constant(source="", location=0, constant="3"),
        center_x=Constant(source="", location=0, constant="4"),
        center_y=Constant(source="", location=0, constant="5"),
        rotation=Constant(source="", location=0, constant="6"),
    ),
    Code22: Code22(
        source="",
        location=0,
        exposure=Constant(source="", location=0, constant="1"),
        width=Constant(source="", location=0, constant="2"),
        height=Constant(source="", location=0, constant="3"),
        x_lower_left=Constant(source="", location=0, constant="4"),
        y_lower_left=Constant(source="", location=0, constant="5"),
        rotation=Constant(source="", location=0, constant="6"),
    ),
    AS: AS(source="", location=0, correspondence=AxisCorrespondence.AX_BY),
    FS: FS(
        source="",
        location=0,
        zeros="L",
        coordinate_mode="A",
        x_integral=2,
        x_decimal=3,
        y_integral=4,
        y_decimal=5,
    ),
    IN: IN(source="", location=0, name="name"),
    IP: IP(source="", location=0, polarity="D"),
    IR: IR(source="", location=0, rotation_degrees=90),
    MI: MI(source="", location=0, a_mirroring=0, b_mirroring=1),
    MO: MO(source="", location=0, mode=UnitMode.METRIC),
    OF: OF(source="", location=0, a_offset=1, b_offset=2),
    SF: SF(source="", location=0, a_scale=1.0, b_scale=1.0),
    File: File(source="", location=0, nodes=[]),
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
