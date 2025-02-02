from __future__ import annotations

from pathlib import Path

from pygerber.common.namespace import Namespace
from test.assets.asset import GerberX3Asset
from test.assets.assetlib import (
    Directory,
    File,
    GitFile,
    ImageAsset,
    ImageFormat,
    TextAsset,
)
from test.assets.reference import REFERENCE_REPOSITORY

THIS_FILE = Path(__file__)
THIS_DIRECTORY = THIS_FILE.parent

THIS_DIRECTORY_SRC = Directory.new(THIS_DIRECTORY)
NAMESPACE = "gerber/flashes"

asset_00_circle_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("00_circle+h_4.grb")
)
asset_00_circle_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/00_circle+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_00_circle_h_4_tbh_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("00_circle+h_4_tbh.grb")
)
asset_00_circle_h_4_tbh_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/00_circle+h_4_tbh.grb.png"),
    ImageFormat.PNG,
)

asset_00_circle_4_grb = TextAsset[File].new(THIS_DIRECTORY_SRC.file("00_circle_4.grb"))
asset_00_circle_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/00_circle_4.grb.png"),
    ImageFormat.PNG,
)

asset_00_circle_4_node_finder_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("00_circle_4_node_finder.grb")
)
asset_00_circle_4_node_finder_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/00_circle_4_node_finder.grb.png"),
    ImageFormat.PNG,
)

asset_01_rectangle_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("01_rectangle+h_4.grb")
)
asset_01_rectangle_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/01_rectangle+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_01_rectangle_v_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("01_rectangle+v+h_4.grb")
)
asset_01_rectangle_v_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/01_rectangle+v+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_01_rectangle_v_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("01_rectangle+v_4.grb")
)
asset_01_rectangle_v_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/01_rectangle+v_4.grb.png"),
    ImageFormat.PNG,
)

asset_01_rectangle_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("01_rectangle_4.grb")
)
asset_01_rectangle_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/01_rectangle_4.grb.png"),
    ImageFormat.PNG,
)

asset_02_obround_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("02_obround+h_4.grb")
)
asset_02_obround_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/02_obround+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_02_obround_v_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("02_obround+v+h_4.grb")
)
asset_02_obround_v_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/02_obround+v+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_02_obround_v_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("02_obround+v_4.grb")
)
asset_02_obround_v_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/02_obround+v_4.grb.png"),
    ImageFormat.PNG,
)

asset_02_obround_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("02_obround_4.grb")
)
asset_02_obround_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/02_obround_4.grb.png"),
    ImageFormat.PNG,
)

asset_03_polygon3_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("03_polygon3+h_4.grb")
)
asset_03_polygon3_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/03_polygon3+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_03_polygon3_r90_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("03_polygon3+r90+h_4.grb")
)
asset_03_polygon3_r90_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/03_polygon3+r90+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_03_polygon3_r90_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("03_polygon3+r90_4.grb")
)
asset_03_polygon3_r90_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/03_polygon3+r90_4.grb.png"),
    ImageFormat.PNG,
)

asset_03_polygon3_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("03_polygon3_4.grb")
)
asset_03_polygon3_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/03_polygon3_4.grb.png"),
    ImageFormat.PNG,
)

asset_04_polygon6_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("04_polygon6+h_4.grb")
)
asset_04_polygon6_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/04_polygon6+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_04_polygon6_r90_h_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("04_polygon6+r90+h_4.grb")
)
asset_04_polygon6_r90_h_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/04_polygon6+r90+h_4.grb.png"),
    ImageFormat.PNG,
)

asset_04_polygon6_r90_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("04_polygon6+r90_4.grb")
)
asset_04_polygon6_r90_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/04_polygon6+r90_4.grb.png"),
    ImageFormat.PNG,
)

asset_04_polygon6_4_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("04_polygon6_4.grb")
)
asset_04_polygon6_4_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/04_polygon6_4.grb.png"),
    ImageFormat.PNG,
)

asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("05_circle+h_rectangle+h_obround+h_traingle+h.grb")
)
asset_05_circle_h_rectangle_h_obround_h_triangle_h_grb_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(
        f"{NAMESPACE}/05_circle+h_rectangle+h_obround+h_traingle+h.grb.png"
    ),
    ImageFormat.PNG,
)


class Flashes(Namespace):
    asset_00_circle_h_4_grb = GerberX3Asset(THIS_DIRECTORY / "00_circle+h_4.grb")
    asset_00_circle_h_4_tbh_grb = GerberX3Asset(
        THIS_DIRECTORY / "00_circle+h_4_tbh.grb"
    )
    asset_00_circle_4_grb = GerberX3Asset(THIS_DIRECTORY / "00_circle_4.grb")
    asset_00_circle_4_node_finder_grb = GerberX3Asset(
        THIS_DIRECTORY / "00_circle_4_node_finder.grb"
    )
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
