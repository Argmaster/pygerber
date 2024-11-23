from __future__ import annotations

from test.assets.assetlib import GitFile, ImageAsset, ImageFormat, SvgImageAsset
from test.assets.reference import REFERENCE_REPOSITORY

CONVERT_PNG_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_png.png"),
    ImageFormat.PNG,
)
CONVERT_JPEG_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_jpg.jpg"),
    ImageFormat.JPEG,
)
CONVERT_TIFF_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_tiff.tiff"),
    ImageFormat.TIFF,
)
CONVERT_BMP_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_bmp.bmp"),
    ImageFormat.BMP,
)
CONVERT_WEBP_LOSSY_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_webp.webp"),
    ImageFormat.WEBP,
)
CONVERT_WEBP_LOSSLESS_REFERENCE_IMAGE = ImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_webp_lossless.webp"),
    ImageFormat.WEBP,
)

CONVERT_SVG_REFERENCE_IMAGE = SvgImageAsset[GitFile].new(
    REFERENCE_REPOSITORY.file("reference/pygerber/console/convert_svg.svg"),
)
