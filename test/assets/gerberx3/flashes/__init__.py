from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent


class Flashes(Namespace):
    asset_00_circle_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "00_circle+h_4.grb")
    asset_00_circle_h_4_tbh_grb = GerberX3Asset(
        THIS_DIRECTORY / "00_circle+h_4_tbh.grb"
    )
    asset_00_circle_4_grb = GerberX3Asset(THIS_DIRECTORY / "00_circle_4.grb")
    asset_01_rectangle_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "01_rectangle+h_4.grb")
    asset_01_rectangle_v_h_4_grb = GerberX3Asset(
        THIS_DIRECTORY / "01_rectangle+v+h_4.grb"
    )
    asset_01_rectangle_v_4_grb = GerberX3Asset(THIS_DIRECTORY / "01_rectangle+v_4.grb")
    asset_01_rectangle_4_grb = GerberX3Asset(THIS_DIRECTORY / "01_rectangle_4.grb")
    asset_02_obround_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "02_obround+h_4.grb")
    asset_02_obround_v_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "02_obround+v+h_4.grb")
    asset_02_obround_v_4_grb = GerberX3Asset(THIS_DIRECTORY / "02_obround+v_4.grb")
    asset_02_obround_4_grb = GerberX3Asset(THIS_DIRECTORY / "02_obround_4.grb")
    asset_03_polygon3_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "03_polygon3+h_4.grb")
    asset_03_polygon3_r90_h_4_grb = GerberX3Asset(
        THIS_DIRECTORY / "03_polygon3+r90+h_4.grb"
    )
    asset_03_polygon3_r90_4_grb = GerberX3Asset(
        THIS_DIRECTORY / "03_polygon3+r90_4.grb"
    )
    asset_03_polygon3_4_grb = GerberX3Asset(THIS_DIRECTORY / "03_polygon3_4.grb")
    asset_04_polygon6_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "04_polygon6+h_4.grb")
    asset_04_polygon6_r90_h_4_grb = GerberX3Asset(
        THIS_DIRECTORY / "04_polygon6+r90+h_4.grb"
    )
    asset_04_polygon6_r90_4_grb = GerberX3Asset(
        THIS_DIRECTORY / "04_polygon6+r90_4.grb"
    )
    asset_04_polygon6_4_grb = GerberX3Asset(THIS_DIRECTORY / "04_polygon6_4.grb")
    asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb = GerberX3Asset(
        THIS_DIRECTORY / "05_circle+h_rectangle+h_obround+h_traingle+h.grb"
    )
