from __future__ import annotations

from pathlib import Path

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
NAMESPACE = "gerber/A64_OLinuXino_rev_G"


A64_OlinuXino_Rev_G_B_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-B_Cu.gbr")
)
A64_OlinuXino_Rev_G_B_Cu_Formatted = TextAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-B_Cu.formatted.gbr")
)
A64_OlinuXino_Rev_G_B_Cu_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-B_Cu.png"),
    ImageFormat.PNG,
)
A64_OlinuXino_Rev_G_B_Cu_png_shapely = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-B_Cu.shapely.png"),
    ImageFormat.PNG,
)

A64_OlinuXino_Rev_G_B_Mask = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-B_Mask.gbr")
)
A64_OlinuXino_Rev_G_B_Mask_Formatted = TextAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-B_Mask.formatted.gbr")
)
A64_OlinuXino_Rev_G_B_Mask_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-B_Mask.png"),
    ImageFormat.PNG,
)


A64_OlinuXino_Rev_G_B_Paste = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-B_Paste.gbr")
)

A64_OlinuXino_Rev_G_B_SilkS = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-B_SilkS.gbr")
)

A64_OlinuXino_Rev_G_Edge_Cuts = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-Edge_Cuts.gbr")
)

A64_OlinuXino_Rev_G_F_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-F_Cu.gbr")
)
A64_OlinuXino_Rev_G_F_Cu_Formatted = TextAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-F_Cu.formatted.gbr")
)
A64_OlinuXino_Rev_G_F_Cu_png = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-F_Cu.png"),
    ImageFormat.PNG,
)
A64_OlinuXino_Rev_G_F_Cu_png_shapely = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file(f"{NAMESPACE}/A64-OlinuXino_Rev_G-F_Cu.shapely.png"),
    ImageFormat.PNG,
)

A64_OlinuXino_Rev_G_F_Mask = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-F_Mask.gbr")
)

A64_OlinuXino_Rev_G_F_Paste = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-F_Paste.gbr")
)

A64_OlinuXino_Rev_G_F_SilkS = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-F_SilkS.gbr")
)

A64_OlinuXino_Rev_G_In1_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-In1_Cu.gbr")
)

A64_OlinuXino_Rev_G_In2_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-In2_Cu.gbr")
)

A64_OlinuXino_Rev_G_In3_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-In3_Cu.gbr")
)

A64_OlinuXino_Rev_G_In4_Cu = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-In4_Cu.gbr")
)

A64_OlinuXino_Rev_G_NPTH = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-NPTH.drl")
)

A64_OlinuXino_Rev_G_PTH = TextAsset[File].new(
    THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-PTH.drl")
)

gbrjob = TextAsset[File].new(THIS_DIRECTORY_SRC.file("A64-OlinuXino_Rev_G-job.gbrjob"))
